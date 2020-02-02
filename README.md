# clash-graph

This is a tool to scrape the Clash Royale API and build a graph database from the results.

## Configuration

### Installation

Use the environment.yml file to create a conda environment with all of the requirements.

### API Key

You will need to request an API key from https://royaleapi.com.  See instructions [here](https://docs.royaleapi.com/#/authentication).

Once you have requested an API key create an environment variable called CLASH_API.

On a *nix environment you can set the environment variable using this command:

```sh
export CLASH_API="<your_api_key_here"
```

### Starting the Database

clash-graph uses a neo4j instance running on a local docker container by default.

You must have docker running on your local machine.

To start neo4j use the following command:

```sh
docker-compose up
```

### Scraping your Clan

Update the clans list in the scrape.py file to start scraping your clans data.

```Python
clans = ["<your_clans_tag>"]
```

## Start Scraping

Run the following command to start the script:

```sh
python scrape.py
```

## Querying Data

clash-graph currently does not have any built in querying functionality.  There are several example queries located at queries.cyp that you can run in the neo4j browser at http://localhost:7474.  See the docker-compose file for the username/password.

