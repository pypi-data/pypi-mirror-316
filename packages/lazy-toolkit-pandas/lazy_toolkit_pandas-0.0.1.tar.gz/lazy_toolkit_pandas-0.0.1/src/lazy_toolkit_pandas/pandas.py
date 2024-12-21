import os
from datetime import tzinfo
from typing import Any, Iterable

import pandas as pd

from lazy_toolkit.enum import Frequency


def df_to_pkl(df: pd.DataFrame,
              filename: str,
              parent_folder_path: str):
    """Save DataFrame to pickle file
    """
    file_path: str = os.path.join(parent_folder_path, filename)

    os.makedirs(parent_folder_path, exist_ok=True)
    df.to_pickle(file_path)


def pkl_to_df(filename: str,
              parent_folder_path: str,
              time_series_column: str | None = None,
              index_is_time_series: bool = False,
              as_tz: tzinfo | None = None,
              remove_tz_info: bool = True) -> pd.DataFrame | None:
    """Load pickle file to DataFrame
    """
    file_path: str = os.path.join(parent_folder_path, filename)

    if not os.path.isfile(file_path):
        return None
    df: pd.DataFrame | None = pd.read_pickle(file_path)
    if df is None:
        return None

    if time_series_column or index_is_time_series:
        if as_tz:
            if time_series_column:
                df[time_series_column] = df[time_series_column].dt.tz_localize(as_tz)
            else:
                df.index = df.index.tz_localize(as_tz)  # type: ignore
        if remove_tz_info:
            if time_series_column:
                df[time_series_column] = df[time_series_column].dt.tz_localize(None)
            else:
                df.index = df.index.tz_localize(None)  # type: ignore
    return df


def df_to_csv(df: pd.DataFrame | None,
              filename: str,
              parent_folder_path: str,
              append: bool = False,
              keep_index: bool = False):
    """Save DataFrame to CSV file, or append to the existing file

    Args:
        append (bool): Whether to append to the existing file or overwrite it
        keep_index (bool): If index column should be also persisted
    """
    if df is None:
        return

    file_path: str = os.path.join(parent_folder_path, filename)

    os.makedirs(parent_folder_path, exist_ok=True)
    if append and os.path.isfile(file_path):
        df.to_csv(file_path, mode='a', header=False, index=keep_index)
    else:
        df.to_csv(file_path, index=keep_index)


def csv_to_df(filename: str,
              parent_folder_path: str,
              index_name: str | None = None,
              time_series_column: str | None = None,
              index_is_time_series: bool = False,
              as_tz: tzinfo | None = None,
              remove_tz_info: bool = True,
              head: int = 0,
              tail: int = 0) -> pd.DataFrame | None:
    """Load CSV file to DataFrame

    Args:
        index_name (str): The name of the index column, if None, then the index will be the default integer index
        time_series_column (str): The name of the time series column, if provided, convert the column to pd.datetime
        index_is_time_series (bool): Whether try to parse the index column as datetime
        as_tz (tzinfo): if provided, convert the time series column (or time series index) to the desired timezone, if None, keep the original datetime
        remove_tz_info (bool): Whether to remove timezone info from the index
        head (int): The number of rows to read from the beginning
        tail (int): The number of rows to read from the end
    """
    file_path: str = os.path.join(parent_folder_path, filename)

    if not os.path.isfile(file_path):
        return None

    # Add option `float_precision='round_trip'` to avoid float precision issue
    # - https://stackoverflow.com/questions/47368296/pandas-read-csv-file-with-float-values-results-in-weird-rounding-and-decimal-dig
    # - https://stackoverflow.com/questions/36909368/precision-lost-while-using-read-csv-in-pandas#comment61383096_36909497
    df: pd.DataFrame | None = None
    if head <= 0 and tail <= 0:
        df = pd.read_csv(file_path, index_col=index_name, parse_dates=index_is_time_series, float_precision='round_trip')

    # TODO: improve the performance by reading the file in reverse order
    if head > 0:
        df = pd.read_csv(file_path, index_col=index_name, parse_dates=index_is_time_series, float_precision='round_trip')\
            .head(head)
    if tail > 0:
        df = pd.read_csv(file_path, index_col=index_name, parse_dates=index_is_time_series, float_precision='round_trip')\
            .tail(tail)

    if df is None:
        return None

    # Convert the time series column to datetime if it's provided
    if time_series_column:
        df[time_series_column] = pd.to_datetime(df[time_series_column])

    # If there is time series column or index is time series, check if need to convert/remove the timezone info
    if index_is_time_series or time_series_column:
        if as_tz:
            if index_name:
                df.index = df.index.tz_convert(as_tz)  # type: ignore
            elif time_series_column:
                df[time_series_column] = df[time_series_column].dt.tz_convert(as_tz)

        if remove_tz_info:
            if index_name:
                df.index = df.index.tz_localize(None)  # type: ignore
            elif time_series_column:
                df[time_series_column] = df[time_series_column].dt.tz_localize(None)
    return df


def row_filter(df: pd.DataFrame, column: str, filter_values: Iterable[Any], blacklist: bool = True) -> pd.DataFrame:
    """行过滤器，根据提供的 `filter_values` 列表过滤 `column` 列
    - 若 black_list=True，则为黑名单模式，过滤掉 `filter_values` 中的值
    - 若 black_list=False，则为白名单模式，只保留 `filter_values` 中的值
    """
    if blacklist:
        return df[~df[column].isin(set(filter_values))]
    else:
        return df[df[column].isin(set(filter_values))]


def do_resample(df: pd.DataFrame,
                target_freq: Frequency,
                rules: dict[Any, str],
                time_series_column: str | None,
                drop_na: bool = False) -> pd.DataFrame:
    """最基础的重采样函数，将 OHLCV 数据框重采样到目标频率，返回重采样后的 OHLCV 数据
    - 默认只对 `DEFAULT_RESAMPLE_COLUMNS` 中的列进行重采样，若 `more_columns` 为空，则只返回这些列
    - 不修改原 df 的数据

    Args:
        target_freq (KlineFrequency): Returned frequency for resampled data
        time_series_column (str): The name of the time series column, leave it None if the index itself is the time series
        more_columns (dict[str, str]): Additional columns to be aggregated
    """
    if rules is None:
        rules = dict()
    if time_series_column:
        df.set_index(time_series_column, inplace=True)

    res: pd.DataFrame = df.resample(rule=target_freq.as_pandas_offset(),
                                    label='left',
                                    closed='left').aggregate(rules)
    # If `time_series_column` is provided, reset the index on both original DF and resampled DF
    if time_series_column:
        res.reset_index(inplace=True)
        df.reset_index(inplace=True)

    if drop_na:
        res = res.dropna()

    return res


def do_resamples(df: pd.DataFrame,
                 target_freqs: list[Frequency],
                 rules: dict[Any, str],
                 time_series_column: str | None) -> dict[str, pd.DataFrame]:
    """Do resample for multiple target frequencies, return a dictionary of resampled data frames with different frequencies as keys
    """
    res: dict[str, pd.DataFrame] = dict()
    for freq in target_freqs:
        res[freq.value] = do_resample(df, freq, rules, time_series_column)
    return res


def do_resample_with_offset(df: pd.DataFrame,
                            rules: dict[Any, str],
                            data_freq: Frequency,
                            offset_freq: Frequency,
                            offset_col: str | None,
                            time_series_column: str | None) -> pd.DataFrame:
    """对数据进行重采样，以目标频率和偏移量为参数
    - E.g.：如果数据频率是 1h，目标频率是 12h，则将数据重采样为 12h，但是会有 12 个不同的偏移量 (0h ~ 11h)

    样例：在分析 12 小时的 K 线数据时。默认情况下，重采样可能会在每天的上午 8 点到下午 8 点之间进行，但是如果在晚上 10 点发生了重要的市场事件，
    那么关于该事件的信息将被忽略。通过引入偏移量计算（例如从上午 9 点开始），就可以捕获该事件并将其包含在分析中。

    Args:
        offset_freq (KlineFrequency): 重采样的目标频率，同时也决定了偏移量的计算
        offset_col (str): 重采样偏移量的列名，如果不提供则默认为 'offset'
        time_series_column (str): The name of the time series column, leave it None if the index itself is the time series
        more_columns (dict[str, str]): Additional columns to be aggregated
    """
    if not offset_col:
        offset_col = 'offset'

    # 根据数据频率和目标频率计算偏移量，举例：
    # - 如果数据频率是 1h，目标频率是 12h，则 pandas_offset = '12h', offset_count = 12, offset_unit = 'h'
    #   - 即 0h ~ 11h 共 12 个偏移量操作
    # - 如果数据频率是 15m，目标频率是 1h，则 pandas_offset = '1h', offset_count = 4, offset_unit = 'm'
    #   - 即 0min, 15min, 30min, 45min 共 4 个偏移量操作
    offset_count: int = offset_freq.to_minutes() // data_freq.to_minutes()

    # If target frequency is less precise than data frequency, return the resampled data directly
    if offset_count <= 1:
        resampled: pd.DataFrame = do_resample(df, offset_freq, rules, time_series_column)
        resampled[offset_col] = pd.NA
        return resampled

    if time_series_column:
        df.set_index(time_series_column, inplace=True)

    offset_unit: str = data_freq.as_pandas_offset()[-1]
    offset_value_per_count: int = int(data_freq.as_pandas_offset()[:-1])
    res: list[pd.DataFrame] = list()
    for offset in [i * offset_value_per_count for i in range(offset_count)]:
        offset_str: str = f'{offset}{offset_unit}'
        period_df = df.resample(rule=offset_freq.as_pandas_offset(),
                                offset=offset_str).aggregate(rules)
        period_df[offset_col] = offset
        if time_series_column:
            period_df.reset_index(inplace=True)
        res.append(period_df)

    # Merge all the period data frames and sort by time series
    period_df = pd.concat(res, ignore_index=True)
    if time_series_column:
        df.reset_index(inplace=True)
        period_df.sort_values(by=time_series_column, inplace=True)
    else:
        period_df.sort_index(inplace=True)

    return period_df


def do_resample_for_indicator(df: pd.DataFrame,
                              target_freq: Frequency,
                              rules: dict[Any, str],
                              time_series_column: str | None,
                              indicator_column: str) -> pd.DataFrame:
    """Do resample for data with a indicator column and return the resampled data frame

    Args:
        time_series_column (str): The name of the time series column, leave it None if the index itself is the time series
        indicator_column (str): The name of the indicator column
    """
    more_columns: dict[str, str] = {
        indicator_column: 'last',
    }
    resampled_df: pd.DataFrame = do_resample(df, target_freq, rules, time_series_column)
    if resampled_df.empty:
        last_val: Any = df[indicator_column].iloc[-1]
        resampled_df = pd.DataFrame({indicator_column: [last_val]},
                                    index=[df[time_series_column].iloc[-1]])
    return resampled_df


def do_resamples_for_indicator(df: pd.DataFrame,
                               target_freqs: list[Frequency],
                               rules: dict[Any, str],
                               time_series_column: str | None,
                               indicator_column: str) -> dict[str, pd.DataFrame]:
    """Do resample for multiple target frequencies for data with indicator column and return the resampled data frames
    """
    res: dict[str, pd.DataFrame] = dict()
    for freq in target_freqs:
        res[freq.value] = do_resample_for_indicator(df, freq, rules, time_series_column, indicator_column)
    return res
