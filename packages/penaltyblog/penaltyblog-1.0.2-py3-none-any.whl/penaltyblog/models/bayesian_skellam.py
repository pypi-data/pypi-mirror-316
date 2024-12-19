from typing import Dict

import numpy as np
from scipy.stats import poisson

from .base_bayesian_model import BaseBayesianGoalModel
from .football_probability_grid import FootballProbabilityGrid


class BayesianSkellamGoalModel(BaseBayesianGoalModel):
    """Bayesian Skellam Model for Predicting Soccer Matches"""

    STAN_MODEL = """
    data {
        int<lower=0> N;                   // Number of games
        int<lower=1> n_teams;             // Number of teams
        array[N] int goals_home;          // home goals scored
        array[N] int goals_away;          // away goals scored
        array[N] int<lower=1,upper=n_teams> home_team;  // home team indices
        array[N] int<lower=1,upper=n_teams> away_team;  // away team indices
        vector[N] weights;                // match weights
    }

    parameters {
        real home;            // Home advantage effect
        vector[n_teams] attack;       // Attack strength per team
        vector[n_teams] defence;      // Defense strength per team
    }

    model {
        // Priors
        home ~ normal(0, 1);
        attack ~ normal(0, 0.5);
        defence ~ normal(0, 0.5);

        // Likelihood
        for (i in 1:N) {
            real lambda_home = exp(home + attack[home_team[i]] - defence[away_team[i]]);
            real lambda_away = exp(attack[away_team[i]] - defence[home_team[i]]);

            target += weights[i] * poisson_lpmf(goals_home[i] | lambda_home);
            target += weights[i] * poisson_lpmf(goals_away[i] | lambda_away);
        }
    }

    generated quantities {
        vector[N] goal_difference;
        for (i in 1:N) {
            goal_difference[i] = goals_home[i] - goals_away[i];
        }
    }
    """

    def _get_model_parameters(self):
        draws = self.fit_result.draws_pd()
        att_params = [x for x in draws.columns if "attack" in x]
        defs_params = [x for x in draws.columns if "defence" in x]
        return draws, att_params, defs_params

    def _format_team_parameters(self, draws, att_params, defs_params):
        attack = [None] * self.n_teams
        defence = [None] * self.n_teams
        team = self.teams["team"].tolist()

        atts = draws[att_params].mean()
        defs = draws[defs_params].mean()

        for idx, _ in enumerate(team):
            attack[idx] = round(atts.iloc[idx], 3)
            defence[idx] = round(defs.iloc[idx], 3)

        return team, attack, defence

    def __repr__(self):
        repr_str = "Module: Penaltyblog\n\nModel: Bayesian Skellam (Stan)\n\n"

        if not self.fitted:
            return repr_str + "Status: Model not fitted"

        draws, att_params, defs_params = self._get_model_parameters()
        team, attack, defence = self._format_team_parameters(
            draws, att_params, defs_params
        )

        repr_str += f"Number of parameters: {len(att_params) + len(defs_params) + 2}\n"
        repr_str += "{0: <20} {1:<20} {2:<20}".format("Team", "Attack", "Defence")
        repr_str += "\n" + "-" * 60 + "\n"

        for t, a, d in zip(team, attack, defence):
            repr_str += "{0: <20} {1:<20} {2:<20}\n".format(t, a, d)

        repr_str += "-" * 60 + "\n"
        repr_str += f"Home Advantage: {round(draws['home'].mean(), 3)}\n"

        return repr_str

    def fit(self, draws=5000, warmup=2000):
        """
        Fits the Bayesian Bivariate Goal Model to the provided match data.

        Args:
            draws (int, optional): Number of posterior draws to generate, defaults to 5000.
            warmup (int, optional): Number of warmup draws, defaults to 2000.
        """
        data = {
            "N": len(self.fixtures),
            "n_teams": len(self.teams),
            "goals_home": self.fixtures["goals_home"].values,
            "goals_away": self.fixtures["goals_away"].values,
            "home_team": self.fixtures["home_index"].values,
            "away_team": self.fixtures["away_index"].values,
            "weights": self.fixtures["weights"].values,
        }

        self._compile_and_fit_stan_model(self.STAN_MODEL, data, draws, warmup)
        return self

    def get_params(self) -> Dict:
        """
        Returns the fitted parameters of the Bayesian Bivariate Goal Model.

        Returns:
            dict: A dictionary containing the fitted parameters of the model.
        """
        if not self.fitted:
            raise ValueError("Model must be fit before getting parameters")

        draws = self.fit_result.draws_pd()
        team_names = self.teams["team"].tolist()
        attack = draws.filter(like="attack").mean().values
        defence = draws.filter(like="defence").mean().values

        params = {
            "teams": team_names,
            "attack": dict(zip(team_names, np.round(attack, 3))),
            "defence": dict(zip(team_names, np.round(defence, 3))),
            "home_advantage": round(draws["home"].mean(), 3),
        }
        return params

    def predict(
        self, home_team: str, away_team: str, max_goals: int = 15, n_samples: int = 1000
    ) -> FootballProbabilityGrid:
        """
        Predicts the probability of goals scored by a home team and an away team.

        Args:
            home_team (str): The name of the home team.
            away_team (str): The name of the away team.
            max_goals (int, optional): The maximum number of goals to consider, defaults to 15.
            n_samples (int, optional): The number of samples to use for prediction, defaults to 1000.

        Returns:
                FootballProbabilityGrid: A FootballProbabilityGrid object containing
                the predicted probabilities.
        """
        if not self.fitted:
            raise ValueError("Model must be fit before making predictions")

        draws = self.fit_result.draws_pd()
        home_idx = self._get_team_index(home_team)
        away_idx = self._get_team_index(away_team)
        samples = draws.sample(n=n_samples, replace=True)

        lambda_home = np.exp(
            samples["home"]
            + samples[f"attack[{home_idx}]"]
            - samples[f"defence[{away_idx}]"]
        )

        lambda_away = np.exp(
            samples[f"attack[{away_idx}]"] - samples[f"defence[{home_idx}]"]
        )

        home_probs = poisson.pmf(np.arange(max_goals + 1)[:, None], lambda_home.values)
        away_probs = poisson.pmf(
            np.arange(max_goals + 1)[None, :], lambda_away.values[:, None]
        )
        score_probs = np.tensordot(home_probs, away_probs, axes=(1, 0)) / n_samples

        home_expectancy = np.sum(score_probs.sum(axis=1) * np.arange(max_goals + 1))
        away_expectancy = np.sum(score_probs.sum(axis=0) * np.arange(max_goals + 1))

        return FootballProbabilityGrid(score_probs, home_expectancy, away_expectancy)

    def _get_team_index(self, team_name):
        idx = self.teams.loc[self.teams["team"] == team_name, "team_index"]
        if idx.empty:
            raise ValueError(f"Team {team_name} not found.")
        return idx.iloc[0] - 1
