import numpy as np
import pandas as pd
from .fast_transformers import calculate_log_returns, calculate_returns


class PortfolioSimulator ():
    """
    A simulator for managing and evaluating a financial portfolio.

    Attributes:
        initial_cash (float): Initial cash available for investments.
        target_weight (float): Target allocation weight for the portfolio.
        df (DataFrame): A DataFrame containing historical prices of assets.
        manager (object): An object responsible for risk management. Must implement a `check_risk` method.
            The `check_risk` method takes the simulator object as a parameter and uses its attributes (e.g., `history`, `positions`) to return:
                1. A dictionary where keys are tickers in `simulator.positions` and values are True (keep the asset) or False (sell the asset).
                2. A dictionary with detailed metrics and rationale for each ticker.
        verbose (int): Verbosity level (0 for silent, 1 for monitoring outputs).
        liquid_money (float): Current uninvested cash.
        portfolio_value (float): Total value of the portfolio (cash + investments).
        history (list): A log of all portfolio actions and changes.
        balancing_dates (list): Dates when rebalancing occurred.
        trades (dict): A dictionary logging trades by date.
        positions (dict): Current holdings in the portfolio with allocation and amount details.
    """
    def __init__ (self, initial_cash, target_weight, df, manager=None, verbose=1):
        """
        Initialize the PortfolioSimulator.

        Args:
            initial_cash (float): Initial cash for the portfolio.
            target_weight (float): Target allocation weight for the portfolio.
            df (DataFrame): A DataFrame containing historical prices of assets.
            manager (object): Risk manager object with a `check_risk` method.
            verbose (int): Verbosity level (0 for silent, 1 for monitoring outputs).

        Raises:
            ValueError: If `verbose` is not 0 or 1.
        """
        if verbose not in [1, 0]:
            raise ValueError(f"Verbose parameter must be 0 (silent) or 1 (monitor)")
        self.initial_cash=initial_cash
        self.liquid_money=initial_cash
        self.portfolio_value=initial_cash
        self.target_weight=target_weight
        self.manager = manager
        self.df = df
        self.verbose=verbose
        self.history = []
        self.balancing_dates = []
        self.trades = {}
        self.positions={}
    def simulate (self, signals):
        """
        Simulate portfolio management over time based on buy signals.

        Args:
            signals (dict): A dictionary of buy signals where keys are dates
                and values are lists of assets to buy on those dates.
        """
        initial_date = list(signals.keys())[0]
        self.dates = [date.strftime("%Y-%m-%d") for date in self.df.loc[self.df.index>=initial_date].index]
        self.value = []
        for date_idx, date in enumerate(self.dates):
            if self.verbose==1:
                print (f"\n\n\n---------------------------------{date}: {self.portfolio_value}-----------------------------------")
            self.trades[date] = []
            if date_idx==0:
                self._rebalance(date=date, buy_signals=signals[date])
                self._update_history(date=date, rebalance=True)
            else:
                self.value.append({
                    'Date': date,
                    'Value':self.portfolio_value
                })
                self._update_portfolio_value(date=date)
                self._refresh_positions(date=date)
                
                if self.manager:
                    decision, details = self.manager.check_risk(simulator=self, date=date)
                    for key, value in decision.items():
                        if self.verbose==1:
                            print (f"\nDecision")
                            print (key, value)
                            print (f"{details[key]}")
                    
                    sold_assets = []
                    for asset in decision:
                        if not decision[asset]:
                            sold_assets.append(asset)
                            self._sell_(asset=asset, quantity=True, date=date)
                        
                if date in list(signals.keys()):
                    self._rebalance(date=date, buy_signals=signals[date])
                    self._update_history(date=date, rebalance=True)
                else:
                    self._update_history(date=date, rebalance=False)
    def _refresh_positions (self, date):
        """
        Update positions based on the most recent prices and calculate new allocations.

        Args:
            date (str): The date for which to refresh positions.
        """
        date_idx = self.dates.index(date)
        last_date_record = pd.DataFrame(self.history).loc[(pd.DataFrame(self.history)['Date'] == self.dates[date_idx-1])&(pd.DataFrame(self.history)['Sell Hour (UTC-6)']=='--')]
        assets = last_date_record['Asset'].unique().tolist()
        prices_df = self.df.loc[[self.dates[date_idx-1], self.dates[date_idx]], assets]
        date_return = calculate_returns(array=prices_df.values, period=1).reshape(-1,) + 1
        self.positions = {}
        for asset_idx, asset in enumerate(last_date_record['Asset'].unique()):
            self.positions[asset] = {
                'Allocation': last_date_record.loc[last_date_record['Asset']==asset]['Amount'].values[0] * date_return[asset_idx] / self.portfolio_value,
                'Amount': last_date_record.loc[last_date_record['Asset']==asset]['Amount'].values[0] * date_return[asset_idx]
            }
    
    def _update_history(self, date, rebalance):
        """
        Log the portfolio state and transactions to history.

        Args:
            date (str): The date of the update.
            rebalance (bool): Whether rebalancing occurred on this date.
        """
        if rebalance:
            if len(self.history)==0:
                for asset in self.positions:
                        self.history.append({
                                    'Date' : date,
                                    'Asset' : asset,
                                    'Buy Hour (UTC-6)': '13:50',
                                    'Sell Hour (UTC-6)': '--',
                                    'Allocation': self.positions[asset]['Allocation'],
                                    'Amount': self.positions[asset]['Amount'],
                                    'Asset Price': self.df.loc[date, asset]
                                })
            else:
                date_idx = self.dates.index(date)
                last_date_record = pd.DataFrame(self.history).loc[(pd.DataFrame(self.history)['Date']==self.dates[date_idx-1])&(pd.DataFrame(self.history)['Sell Hour (UTC-6)']=='--')]
                assets = last_date_record['Asset'].unique().tolist()
                if len(assets)!=0:
                    prices_df = self.df.loc[[self.dates[date_idx-1], self.dates[date_idx]], assets]
                    date_return = calculate_returns(array=prices_df.values, period=1).reshape(-1,) + 1
                    for asset_idx, asset in enumerate(assets):
                        self.history.append({
                            'Date': self.dates[date_idx-1],
                            'Asset': asset,
                            'Buy Hour (UTC-6)': '--',
                            'Sell Hour (UTC-6)':'13:45',
                            'Allocation': last_date_record.loc[last_date_record['Asset']==asset]['Amount'].values[0] * date_return[asset_idx] / self.portfolio_value,
                            'Amount': last_date_record.loc[last_date_record['Asset']==asset]['Amount'].values[0] * date_return[asset_idx],
                            'Asset Price': self.df.loc[date, asset]
                        })
                    for asset in self.positions:
                        self.history.append({
                                    'Date' : date,
                                    'Asset' : asset,
                                    'Buy Hour (UTC-6)': '13:50',
                                    'Sell Hour (UTC-6)': '--',
                                    'Allocation': self.positions[asset]['Allocation'],
                                    'Amount': self.positions[asset]['Amount'],
                                    'Asset Price': self.df.loc[date, asset]
                                })
                else:
                    for asset in self.positions:
                        self.history.append({
                                    'Date' : date,
                                    'Asset' : asset,
                                    'Buy Hour (UTC-6)': '13:50',
                                    'Sell Hour (UTC-6)': '--',
                                    'Allocation': self.positions[asset]['Allocation'],
                                    'Amount': self.positions[asset]['Amount'],
                                    'Asset Price': self.df.loc[date, asset]
                                })

        else:
            date_idx = self.dates.index(date)
            last_date_record = pd.DataFrame(self.history).loc[(pd.DataFrame(self.history)['Date']==self.dates[date_idx-1])&(pd.DataFrame(self.history)['Sell Hour (UTC-6)'] == '--')]
            last_date_record_assets = last_date_record['Asset'].unique().tolist()
            
            if len (last_date_record_assets) == 0:
                self.history.append({
                    'Date': date,
                    'Asset': np.nan,
                    'Buy Hour (UTC-6)': np.nan,
                    'Sell Hour (UTC-6)': np.nan,
                    'Allocation': np.nan,
                    'Amount': np.nan,
                    'Asset Price': np.nan
                })
            else:
                prices_df = self.df.loc[[self.dates[date_idx-1], self.dates[date_idx]], last_date_record_assets]
                date_return = calculate_returns(array=prices_df.values, period=1).reshape(-1,) + 1
                sold_assets = []
                for asset in last_date_record_assets:
                    if asset not in self.positions:
                        sold_assets.append(asset)
                if len(sold_assets)==0:
                    for asset_idx, asset in enumerate(last_date_record_assets):
                        self.history.append({
                            'Date': date,
                            'Asset': asset,
                            'Buy Hour (UTC-6)': '--',
                            'Sell Hour (UTC-6)':'--',
                            'Allocation': last_date_record.loc[last_date_record['Asset']==asset]['Amount'].values[0] * date_return[asset_idx] / self.portfolio_value,
                            'Amount': last_date_record.loc[last_date_record['Asset']==asset]['Amount'].values[0] * date_return[asset_idx],
                            'Asset Price': self.df.loc[self.dates[date_idx], asset]
                        })
                else:
                    for asset_idx, asset in enumerate(last_date_record_assets):
                        if asset in sold_assets:
                            self.history.append({
                                'Date': date,
                                'Asset': asset,
                                'Buy Hour (UTC-6)': '--',
                                'Sell Hour (UTC-6)': '13:45',
                                'Allocation': last_date_record.loc[last_date_record['Asset']==asset]['Amount'].values[0] * date_return[asset_idx] / self.portfolio_value,
                                'Amount': last_date_record.loc[last_date_record['Asset']==asset]['Amount'].values[0] * date_return[asset_idx],
                                'Asset Price': self.df.loc[self.dates[date_idx], asset]
                            })
                        else:
                            self.history.append({
                                'Date':date,
                                'Asset': asset,
                                'Buy Hour (UTC-6)': '--',
                                'Sell Hour (UTC-6)': '--',
                                'Allocation': last_date_record.loc[last_date_record['Asset']==asset]['Amount'].values[0] * date_return[asset_idx] / self.portfolio_value,
                                'Amount': last_date_record.loc[last_date_record['Asset']==asset]['Amount'].values[0] * date_return[asset_idx],
                                'Asset Price': self.df.loc[self.dates[date_idx], asset]
                            })

    def _update_portfolio_value(self, date):
        """
        Update the total portfolio value based on current prices and holdings.

        Args:
            date (str): The date for which to update the portfolio value.
        """
        date_idx = self.dates.index(date)
        last_date_record = pd.DataFrame(self.history).loc[(pd.DataFrame(self.history)['Date']==self.dates[date_idx-1])&(pd.DataFrame(self.history)['Sell Hour (UTC-6)'] == '--')]
        assets = last_date_record['Asset'].unique().tolist()
        prices_df = self.df.loc[[self.dates[date_idx-1], self.dates[date_idx]], assets]
        date_return = calculate_returns(array=prices_df.values, period=1).reshape(-1,) + 1
        amounts = last_date_record['Amount'].values
        self.portfolio_value = np.dot(amounts, date_return) + self.liquid_money
        
    def _rebalance (self, date, buy_signals):
        """
        Adjust portfolio to meet target weights based on buy signals.

        Args:
            date (str): The date of rebalancing.
            buy_signals (list): List of assets to buy during rebalancing.
        """
        target_weights = self._split_number_into_parts(number=self.target_weight, n=len(buy_signals))
        current_positions = list(self.positions.keys())
        keeping_positions = list(set(current_positions) & set(buy_signals))
        keeping_target_weights = target_weights[:len(keeping_positions)]
        selling_positions = list(set(current_positions) - set(buy_signals))
        buying_positions = list(set(buy_signals)-set(current_positions))
        buying_target_weights = target_weights[len(keeping_positions):]
        if len(selling_positions) != 0:
            for asset_to_sell in selling_positions:
                self._sell_(asset=asset_to_sell, quantity = True, date=date)
        if len(keeping_positions) != 0:
            keeping_selling_positions = []
            keeping_buying_positions = []
            for asset_to_keep, target_weight in zip(keeping_positions, keeping_target_weights):
                if self.positions[asset_to_keep]['Allocation'] > target_weight:
                    keeping_selling_positions.append(asset_to_keep)
                else:
                    keeping_buying_positions.append(asset_to_keep)
            keeping_positions = keeping_selling_positions + keeping_buying_positions
            for asset_to_keep, target_weight in zip(keeping_positions, keeping_target_weights):
                if self.positions[asset_to_keep]['Allocation'] > target_weight:
                    self._sell_(asset=asset_to_keep, quantity=(((self.positions[asset_to_keep]['Allocation']-target_weight)*(self.positions[asset_to_keep]['Amount']))/(self.positions[asset_to_keep]['Allocation'])), date=date)
                elif self.positions[asset_to_keep]['Allocation'] < target_weight:
                    self._buy_ (asset=asset_to_keep, quantity=((target_weight*self.positions[asset_to_keep]['Amount'])/(self.positions[asset_to_keep]['Allocation'])) - self.positions[asset_to_keep]['Amount'], date=date)
        if len (buying_positions) != 0:
            buying_splits = []
            for target_weight in buying_target_weights:
                buying_splits.append(self.portfolio_value * target_weight)
            for asset_to_buy, buying_amount in zip(buying_positions, buying_splits):
                self._buy_(asset=asset_to_buy, quantity=buying_amount, date=date)

    def _sell_ (self, asset, quantity, date):
        """
        Sell a specified quantity of an asset.

        Args:
            asset (str): The asset to sell.
            quantity (float or bool): Quantity to sell. Use True to sell all.
            date (str): The date of the transaction.

        Raises:
            ValueError: If the asset is not in the portfolio or quantity exceeds holding.
        """
        if asset not in self.positions:
            raise ValueError (f"You can't sell {asset} because it's not in the portfolio.")
        if quantity is True:
            self.trades[date].append(f"selling {self.positions[asset]['Amount']} of {asset}")
            if self.verbose==1:
                print (f"selling {self.positions[asset]['Amount']} of {asset} ")
            self.liquid_money += self.positions[asset]['Amount']
            del self.positions[asset]
        else:
            if self.positions[asset]['Amount'] < quantity:
                raise ValueError(f"You can't sell ${quantity} of {asset}, you only have ${self.positions[asset]['Amount']}")
            else:
                self.trades[date].append(f"selling {quantity} of {asset}")
                self.liquid_money += quantity
                self.positions[asset]['Amount'] -= quantity
                self.positions[asset]['Allocation'] = self.positions[asset]['Amount'] / self.portfolio_value

    def _buy_ (self, asset, quantity, date):
        """
        Buy a specified quantity of an asset.

        Args:
            asset (str): The asset to buy.
            quantity (float): Quantity to buy.
            date (str): The date of the transaction.

        Raises:
            ValueError: If there is insufficient cash to make the purchase.
        """
        if self.verbose==1:
            print (f'Buying {quantity} of {asset}')
        self.trades[date].append(f'Buying {quantity} of {asset}')
        if quantity > self.liquid_money:
            if quantity - self.liquid_money < 0.0001:
                quantity = self.liquid_money
            else:
                raise ValueError (f"Cannot buy {quantity} of {asset} because the liquid money is: {self.liquid_money:.2f}")
        self.liquid_money -= quantity
        if asset in self.positions:
            self.positions[asset]['Amount'] += quantity
            self.positions[asset]['Allocation'] = self.positions[asset]['Amount'] / self.portfolio_value 
        else:
            self.positions[asset] = {
                'Allocation': quantity / self.portfolio_value,
                'Amount': quantity
            }
    def _split_number_into_parts(self, number, n):
        """
        Divide a number into approximately equal parts.

        Args:
            number (float): The number to divide.
            n (int): Number of parts.

        Returns:
            list: List of parts.
        """
        base_part = number / n
        remainder = number - base_part * n
        parts = [base_part] * n
        for i in range(int(remainder * n)):
            parts[i] += 1 / n
        return parts

class MonteCarloSimulator:
    """
    A class for simulating scenarios using the Monte Carlo method on a dataset. This simulator
    generates paths based on the mean and standard deviation of an input array and optionally 
    updates the statistics of each feature after every simulation step.

    Attributes
    ----------
    steps : int
        Number of simulation steps (time steps) to generate.
    paths : int
        Number of Monte Carlo simulation paths (scenarios) to generate.

    Methods
    -------
    simulate(X, axis=0, update=False):
        Runs the Monte Carlo simulation on the input data array `X`.
    """

    def __init__(self, steps, paths):
        """
        Initializes the MonteCarloSimulator with the specified number of steps and paths.

        Parameters
        ----------
        steps : int
            The number of time steps in each simulation.
        paths : int
            The number of simulation paths to generate.
        """
        self.steps = steps
        self.paths = paths

    def simulate(self, X, axis=0, update=False):
        """
        Performs Monte Carlo simulations based on the statistics (mean and standard deviation) of the input array `X`.
        
        If `update` is True, the mean and standard deviation are recalculated for each feature at every simulation step.
        
        Parameters
        ----------
        X : np.ndarray
            The input data array used to initialize the simulation's statistics. Must be a 2D array.
        axis : int, optional
            The axis along which to calculate the statistics. Default is 0 (rows).
        update : bool, optional
            If True, updates the mean and standard deviation after each simulation step. Default is False.
        
        Returns
        -------
        simulations : np.ndarray
            A 3D array of shape (steps, paths, features) representing the simulated paths.
        
        Raises
        ------
        ValueError
            If `X` is not a 2D numpy array, contains NaNs, or if `axis` is not 0 or 1.
        """

        axles = [0, 1]
        if not isinstance(X, np.ndarray):
            raise ValueError("X must be an array")
        if X.ndim != 2:
            raise ValueError("Array must be bidimensional")
        if np.isnan(X).any():
            raise ValueError("Array contains NaNs")
        if axis not in axles:
            raise ValueError("Axis out of range")
        axles.remove(axis)
        if update not in [True, False]:
            raise ValueError("update not a boolean parameter")

        if update:
            std = np.zeros((1, self.paths, X.shape[axles[0]]))
            mean = np.zeros((1, self.paths, X.shape[axles[0]]))
            for feature in range(X.shape[axles[0]]):
                std[0, :, feature] = np.repeat(np.std(np.take(X, feature, axis=axles[0])), self.paths)
                mean[0, :, feature] = np.repeat(np.mean(np.take(X, feature, axis=axles[0])), self.paths)
            
            simulations = np.zeros((self.steps, self.paths, X.shape[axles[0]]))
            for step in range(self.steps):
                current_simulations = np.random.normal(loc=mean, scale=std, size=(1, self.paths, X.shape[axles[0]]))
                for feature in range(X.shape[axles[0]]):
                    std[0, :, feature] = np.std(
                        np.concatenate([np.tile(np.take(X, feature, axis=axles[0]).reshape(-1, 1), self.paths),
                                        np.take(current_simulations[0, :, :], feature, axis=1).reshape(1, -1)], axis=0),
                        axis=0
                    )
                    mean[0, :, feature] = np.mean(
                        np.concatenate([np.tile(np.take(X, feature, axis=axles[0]).reshape(-1, 1), self.paths),
                                        np.take(current_simulations[0, :, :], feature, axis=1).reshape(1, -1)], axis=0),
                        axis=0
                    )
                simulations[step, :, :] = current_simulations[0, :, :]

        else:
            std = np.std(X, axis=axis)
            mean = np.mean(X, axis=axis)
            simulations = np.random.normal(loc=mean, scale=std, size=(self.steps, self.paths, X.shape[axles[0]]))

        return simulations
