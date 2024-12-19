import configparser
import os
import subprocess
from pathlib import Path
from typing import Optional, Union

import pandas as pd


def get_project_root() -> Path:
    """get_project_root _summary_

    Returns
    -------
        _description_
    """
    return Path(__file__).resolve().parent.parent.parent


def create_config() -> None:
    """_summary_"""
    config = configparser.ConfigParser()

    # Add sections and key-value pairs
    config["Interface"] = {"host": "localhost:8090", "instance": "myproject", "processor": "realtime"}
    config["Submodule"] = {
        "name": "endurance-flight-software-csw",
        "commit": "54b4874caa00687d9cbb0e0dc0f1ee960111fc0a",
    }

    # Define the path to the configuration file in the 'src' directory of the project
    repo_root = get_project_root()
    config_path = os.path.join(repo_root, "config.ini")

    # Write the configuration to the file
    with open(config_path, "w", encoding="utf-8") as configfile:
        config.write(configfile)


def read_config(requested_values: Optional[dict] = None) -> dict[str, str]:  # type: ignore
    """
    Reads specified values from a configuration file or
    prints the entire file if no values are requested.

    Args:
        requested_values (dict, optional): A dictionary where the keys are section names
        and the values are lists of keys to retrieve.
        If None, the entire configuration file is printed.

    Returns:
        dict: A dictionary with the requested configuration values,
        or an empty dictionary if the entire file is printed.
    """
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Define the path to the configuration file in the 'src' directory of the project
    repo_root = get_project_root()
    config_path = os.path.join(repo_root, "config.ini")
    # Read the configuration file
    config.read(config_path)

    # If no specific values are requested, print the entire configuration file
    if requested_values is None:
        for section in config.sections():
            print(f"[{section}]")
            for key, value in config.items(section):
                print(f"{key} = {value}")
        return {}

    # Initialize a dictionary to store the retrieved values
    config_values = {}

    # Loop through the requested sections and keys to retrieve values
    for section, keys in requested_values.items():
        for key in keys:
            try:
                # Attempt to get the value for the key in the specified section
                value = config.get(section, key)
                config_values[f"{section}.{key}"] = value
            except (configparser.NoSectionError, configparser.NoOptionError):
                # If the section or key does not exist, you can decide how to handle it
                print(f"Warning: Section '{section}' or key '{key}' not found in the configuration file.")

    return config_values


def create_table(name: str, path: Optional[str] = None) -> None:
    """
    Creates a correspondence table for a given data type (e.g., CCF or CDF).
    The table's filename includes the SHA1 of the submodule commit.

    Parameters
    ----------
    name : str
        The name of the data type (e.g., "ccf" or "cdf").
    path : Optional[str]
        Custom path to the data file. If not provided, uses the default path
        derived from the submodule and configuration.
    Returns:
        None
    """
    repo_root = get_project_root()
    config = read_config({"Submodule": ["name", "commit"]})

    submodule_name = config["Submodule.name"]
    expected_commit = config["Submodule.commit"]
    submodule_path = repo_root / submodule_name

    # Validate submodule path and commit
    if not submodule_path.exists() or not submodule_path.is_dir():
        raise FileNotFoundError(f"Submodule path does not exist: {submodule_path}")

    current_commit = get_submodule_commit(submodule_path)
    if current_commit != expected_commit:
        raise ValueError(f"Submodule commit mismatch. Expected: {expected_commit}, Found: {current_commit}")

    # Name of the output table file
    table_name = f"{name}_table_{current_commit}.dat"
    table_path = repo_root / "etc" / "config" / table_name

    # Check if the table already exists
    if table_path.exists():
        print(f"{name.upper()} table already exists: {table_path}")
        return

    # Determine the path to the data file
    data_file_path = submodule_path / "mdb" / f"{name}.dat" if path is None else Path(path)

    if not data_file_path.exists():
        raise FileNotFoundError(f"{name.upper()} file not found at: {data_file_path}")

    fields = get_fields(name)

    # Read and process the data
    print(f"Reading {name.upper()} data from: {data_file_path}")
    data = pd.read_table(data_file_path, names=fields, sep="\t").dropna(axis=1)

    # Save the processed data with the commit SHA1 in the filename
    table_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(table_path, sep="\t", index=False)

    print(f"{name.upper()} table created at: {table_path}")


def get_submodule_commit(submodule_path: Path) -> str:
    """
    Retrieves the current commit hash of the specified submodule.

    Parameters
    ----------
    submodule_path : Path
        The path to the submodule directory.

    Returns
    -------
    str
        The commit hash of the submodule.
    """
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=submodule_path, text=True).strip()
        return commit
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to retrieve the commit for the submodule: {submodule_path}") from e


def get_fields(name: str) -> list[str]:
    """
    Reads a list of fields from a unified configuration file located in the 'etc/config' directory.

    Parameters
    ----------
    name : str
        The name of the section in the configuration file corresponding to the fields
        (e.g., "ccf" for the section "[CCF_FIELDS]").

    Returns
    -------
    list[str]
        A list of fields specified under the corresponding section in the configuration file.

    Raises
    ------
    FileNotFoundError
        If the configuration file does not exist.
    RuntimeError
        If the configuration file is malformed, missing the section, or the 'fields' key.
    """
    repo_root = get_project_root()
    config_dir = repo_root / "etc" / "config"
    config_file = config_dir / "fields.ini"  # Unified file for all sections.

    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_file}")

    config = configparser.ConfigParser()
    config.read(config_file)

    section = f"{name.upper()}_FIELDS"
    try:
        fields = config.get(section, "fields").split(", ")
        return fields
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        raise RuntimeError(
            f"Failed to load fields from section '{section}' in {config_file}; "
            f"ensure it contains a section '{section}' with a 'fields' key."
        ) from e


def process_pas_table_and_merge(
    pas_number: str = "ENKT0021",
    pas_table_path: Optional[Union[str, Path]] = None,
    obpid_path: Optional[Union[str, Path]] = None,
    output_dir: Optional[Path] = None,
    do_write: bool = False,
) -> pd.DataFrame:
    """
    Process the PAS table and OBPID table, filter data, and merge results.

    Args:
        pas_number (str): The PAS_NUMBR value to filter on.
        pas_table_path (Optional[str]): Path to the PAS table file.
        obpid_path (Optional[str]): Path to the OBPID file.
        output_dir (Optional[Path]): Directory to save the resulting table (default is repo_root/etc/config).
        do_write (bool): Whether to write the dataframe to a .dat file.

    Returns:
        pd.DataFrame: A DataFrame with selected and merged columns.

    Raises:
        FileNotFoundError: If the specified or default files are not found.
        ValueError: If the filtering or merging produces unexpected results.
    """

    current_commit = read_config({"Submodule": ["commit"]})["Submodule.commit"]

    # Resolve paths and ensure proper typing
    pas_table_path = (
        Path(pas_table_path)
        if pas_table_path
        else get_project_root() / "etc" / "config" / f"pas_table_{current_commit}.dat"
    )
    obpid_path = Path(obpid_path) if obpid_path else get_project_root() / "etc" / "config" / "obpid_icd.dat"
    output_dir = Path(output_dir) if output_dir else get_project_root() / "etc" / "config"

    # Validate file existence
    for path, name in [(pas_table_path, "PAS table"), (obpid_path, "OBPID table")]:
        if not path.exists():
            raise FileNotFoundError(f"{name} file not found: {path}")

    # Load files and drop empty columns
    pas_table = pd.read_table(str(pas_table_path), sep="\t").dropna(axis=1)
    obpid_table = pd.read_table(str(obpid_path), sep="\t").dropna(axis=1)

    # Validate required columns
    required_pas_cols = {"PAS_NUMBR", "PAS_ALVAL"}
    required_obpid_cols = {"ID", "Name", "Brief", "Size (Bits)"}
    if not required_pas_cols.issubset(pas_table.columns):
        raise ValueError(f"PAS table must contain columns: {required_pas_cols}")
    if not required_obpid_cols.issubset(obpid_table.columns):
        raise ValueError(f"OBPID table must contain columns: {required_obpid_cols}")

    # Filter PAS table
    pas_filtered = pas_table[pas_table["PAS_NUMBR"] == pas_number]
    if pas_filtered.empty:
        raise ValueError(f"No entries found in PAS table for PAS_NUMBR={pas_number}")

    # Merge tables
    merged_df = pd.merge(pas_filtered, obpid_table, left_on="PAS_ALVAL", right_on="ID", how="inner")

    # Sort and select columns
    final_df = merged_df.sort_values(by="ID")[["PAS_ALTXT", "Name", "Brief", "ID", "Size (Bits)"]]

    # Save to output file
    if do_write:
        output_dir.mkdir(parents=True, exist_ok=True)  # Ensure output directory exists
        table_name = f"obpid_table_{current_commit}.dat"
        output_path = output_dir / table_name
        final_df.to_csv(output_path, sep="\t", index=False)

    return final_df
