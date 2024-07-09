# GitHub Copilot | ML & Data Ops

## Get started with Copilot

1. Install the Copilot and Copilot Chat extensions.
2. Open a new folder in VSCode, copy the [sim.py](https://github.com/awaregroup/copilot-dataops/blob/main/sim.py) into your workspace

## Simulate some data

Question: You've been handed the `sim.py` from a data scientist leaving the company, and need to present their work to leadership in 2mins time, what does the code do???

1. Complete the `# TODO:` comments with Copilot
1. Which hyper-parameter is the least reasonable?
1. Add type hints to the functions
1. Run the script and create data
1. Introduce an error to your file, use the `/fix` command to resolve it.

## Exploratory data analysis

1. Use copilot to design a plan for analysis
1. Create an analysis and EDA
1. Translate your graphs to another graphing library
1. Write an executive summary of the findings (with AI) to add to your notebook.
1. Use `gh copilot suggest` to convert your notebook to pdf to send to a business stakeholder
    - Use native VSCode export if dependencies aren't friendly :)

## Model fitting

1. Get copilot to help suggest models to fit
1. Fit a model to the data, plot predictions

## [Extra] Inference for new data

1. Create a streamlit app (or similar) to generate a prediction
1. Create a dockerfile to host the streamlit app
    - (Optional) Run the container locally
    - Try being specific with your container requirements.
1. Create a `deploy.yml` file to deploy the container to a target of your choosing
    - Can you use other deployments you've done as context to help it create a new one?

## [Extra extra] Do some conversions
1. Python <> R
2. SQL <> Python
3. Upgrade package versions
