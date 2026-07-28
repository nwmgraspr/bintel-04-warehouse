# bintel-04-warehouse

[![Workflow Guide](https://img.shields.io/badge/Pro--Guide-pro--analytics--02-green)](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
[![Python 3.14](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](./pyproject.toml)
[![MIT](https://img.shields.io/badge/license-see%20LICENSE-yellow.svg)](./LICENSE)

> Professional Python project: building and populating a smart sales data warehouse using ETVL.

## Project Description

This project focuses on designing a star schema data warehouse
and loading prepared data into it using the ETVL process:
Extract from prepared CSV files, Transform for the warehouse schema,
Verify row counts and integrity, then Load into SQLite.

We work with cleaned smart sales data containing
customers, products, and sales records.

We learn to:

- create a DuckDB data warehouse programmatically
- extract and transform prepared CSV data for the warehouse schema
- verify tables are populated correctly before and after loading
- query the warehouse to confirm data integrity

## Use Your Prepared Data

After running the example,
copy over your data/prepared/ files to use in this project.

## VS Code and DuckDB Files

We've added a new extension to
[**.vscode/extensions.json**](.vscode/extensions.json) to interact with DuckDB.
Accept the recommended extensions and you should get it. If not:

- Open the **Extensions left-side tab** in VS Code.
- Search for: DuckDB
- Install the extension published by **chuckjonas**.

In this project, we create and populate a dw file in the new **artifacts/** folder.
To explore the new DuckDB, open the new **DuckDB left-side tab** in VS Code
and select **smart_sales**.

![Explore DuckDB](docs/images/fig_duckdb_tab.png)

The extension is configured in [**.vscode/settings.json**](.vscode/settings.json).
Change this `settings.json` file to reflect any changes you make, e.g. a new database name.

## Working Files

You'll work with these areas:

- **.vscode/extensions.json** - see the additional "chuckjonas.duckdb" extension
- **.vscode/settings.json** - configure the project DuckDB file (if changes needed)
- **artifacts/** - generated data warehouse file
- **data/prepared** - paste your prepared CSV files (e.g., customers, products, sales)
- **docs/** - provides project narrative and documentation
- **src/bizintel/** - run the examples; copy and paste to your own versions to modify
- **pyproject.toml** - update authorship & links
- **zensical.toml** - update authorship & links

## Instructions (pro-analytics-02)

Follow the
[step-by-step workflow guide](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
to complete:

1. Phase 1. **Start & Run**
2. Phase 2. **Change Authorship**
3. Phase 3. **Read & Understand**
4. Phase 4. **Modify**
5. Phase 5. **Apply**

## Challenges

Challenges are expected.
Sometimes instructions may not quite match your operating system.
When issues occur, share screenshots, error messages, and details about what you tried.
Working through issues is part of implementing professional projects.

## Success

After completing Phase 1. **Start & Run**,
you'll have your own GitHub project,
and running the example module will print out:

```shell
2026-07-27 07:21:40 | INFO | BI | ========================
2026-07-27 07:21:40 | INFO | BI | Executed successfully!
2026-07-27 07:21:40 | INFO | BI | ========================

A new file `project.log` will appear in the root project folder.

## Command Reference

<details>
<summary>Show command reference</summary>

### In a machine terminal (open in your `Repos` folder)

After you get a copy of this repo in your own GitHub account,
open a machine terminal in your `Repos` folder:

```shell
# Replace username with YOUR GitHub username.
git clone https://github.com/nwmgraspr/bintel-04-warehouse

cd bintel-04-warehouse
code .
```

### In a VS Code terminal

These are listed for convenience.
For best results, follow the detailed instructions in
[pro-analytics-02 guide](https://denisecase.github.io/pro-analytics-02/).

```shell
uv self update
uv python pin 3.14
uv lock --upgrade
uv sync --extra dev --extra docs --upgrade

uvx pre-commit install
uvx pre-commit autoupdate

git add -A
uvx pre-commit run --all-files
# repeat if changes were made
uvx pre-commit run --all-files

# verify the environment (.venv/)
uv run python -m bizintel.app_case

# Workflow 1: build an empty data warehouse in artifacts/
uv run python -m bizintel.dw_create_case

# Workflow 3: etl (extract-transform-load) prepared data into dw
uv run python -m bizintel.etl_case

# run common chores
uv run ruff format .
uv run ruff check . --fix
uv run python -m pyright
uv run python -m pytest
uv run python -m zensical build

# save progress
git add -A
git commit -m "update"
git push -u origin main
```
# Custom Run
Run the project scripts in the following order.
### 1. Generate University Dataset
Creates the raw university records source file:
```powershell
uv run python -m bizintel.generate_university_dataset
```
Output:
```
data/raw/university_records.csv
```
---
### 2. Create Data Warehouse
Creates the DuckDB warehouse and required tables:
```powershell
uv run python -m bizintel.dw_create_university
```
Output:
```
artifacts/university_records.duckdb
```
Runs the Extract, Transform, Verify, and Load process:
```powershell
uv run python -m bizintel.etl_university
```
The pipeline:
- Reads `university_records.csv`
- Creates dimension and fact tables
- Loads data into DuckDB
- Verifies successful loading
### Restore / Reset
Remove generated files:
```powershell
git restore artifacts/university_records.duckdb
git restore artifacts/ project.log ```
```
After resetting, rebuild the project by running the three scripts again in order:
```powershell
uv run python -m bizintel.generate_university_dataset
uv run python -m bizintel.dw_create_university
uv run python -m bizintel.etl_university
```

</details>

## Notes

- Use the **UP ARROW** and **DOWN ARROW** in the terminal to scroll through past commands.
- Use `CTRL+f` to find (and replace) text within a file.
- You do not need to add to or modify `tests/`. They are provided for example only.
- Many files are silent helpers. Explore as you like, but nothing is required.
- You do NOT need to understand everything; understanding builds naturally over time.

## Troubleshooting >>>

If you see something like this in your terminal: `>>>` or `...`
You accidentally started Python interactive mode.
It happens.
Press `Ctrl+c` (both keys together) or `Ctrl+Z` then `Enter` on Windows.

## Troubleshooting "File Used By Another Process"

If you try to run Python that interacts with the DuckDB file and get an error that a
file is being used by another process, just
click the **DuckDB left-side tab**, right-click your database and select **Detach Database**.

## Workflow 1. Example Output (Remove or Replace this Section after You Verify)

```shell

========================
START university dataset generation
========================
Created dataset: data\raw\university_records.csv
Rows created: 100
========================
Dataset generation complete
========================
```

## Workflow 2. Example Output (Remove or Replace this Section after You Verify)

```shell
2026-07-28 14:40:13 | INFO | BI | ========================
2026-07-28 14:40:13 | INFO | BI | START create warehouse
2026-07-28 14:40:13 | INFO | BI | ========================
2026-07-28 14:40:13 | INFO | BI | Data warehouse: = artifacts\university_records.duckdb
2026-07-28 14:40:13 | INFO | BI | Connecting to DuckDB warehouse...
2026-07-28 14:40:13 | INFO | BI | Deleting existing warehouse tables...
2026-07-28 14:40:13 | INFO | BI | All existing tables deleted.
2026-07-28 14:40:13 | INFO | BI | Creating dim_students...
2026-07-28 14:40:13 | INFO | BI | dim_students created.
2026-07-28 14:40:13 | INFO | BI | Creating dim_courses...
2026-07-28 14:40:13 | INFO | BI | dim_courses created.
2026-07-28 14:40:13 | INFO | BI | Creating dim_instructors...
2026-07-28 14:40:13 | INFO | BI | dim_instructors created.
2026-07-28 14:40:13 | INFO | BI | START create semesters dimension table....
2026-07-28 14:40:13 | INFO | BI | dim_semesters created.
2026-07-28 14:40:13 | INFO | BI | Creating fact_enrollments...
2026-07-28 14:40:13 | INFO | BI | fact_enrollments created.
2026-07-28 14:40:13 | INFO | BI | Verifying warehouse schema...
2026-07-28 14:40:13 | INFO | BI | Tables in warehouse: ['dim_courses', 'dim_instructors', 'dim_semesters', 'dim_students', 'fact_enrollments']
2026-07-28 14:40:13 | INFO | BI | ========================
2026-07-28 14:40:13 | INFO | BI | University warehouse created successfully.
2026-07-28 14:40:13 | INFO | BI | ========================
```
## Workflow 2. Example Output (Remove or Replace this Section after You Verify)

```shell
=== fact_enrollments ===
    EnrollmentID EnrollmentDate  StudentID  CourseID  InstructorID  SemesterID Grade
0           1001     2024-01-31       1002       110           504           1     A
1           1002     2025-07-28       1004       104           505           1    A-
2           1003     2025-08-26       1009       107           502           2    B+
3           1004     2024-10-11       1001       103           504           3    A-
4           1005     2025-01-24       1004       106           501           1     A
..           ...            ...        ...       ...           ...         ...   ...
95          1096     2025-10-14       1008       108           503           4    B+
96          1097     2025-03-26       1009       108           502           3     A
97          1098     2024-11-23       1005       104           503           3    B-
98          1099     2025-01-27       1002       103           502           4    C+
99          1100     2025-02-21       1003       104           501           2    B+

[100 rows x 7 columns]
2026-07-28 14:43:51 | INFO | BI | ========================
2026-07-28 14:43:51 | INFO | BI | University ETL completed successfully.
2026-07-28 14:43:51 | INFO | BI | ========================
```


## Project Documentation

Additional project instructions, terms, and notes:

[docs/index.md](docs/index.md)

## Citation

[CITATION.cff](./CITATION.cff)

## License

[MIT](./LICENSE)
