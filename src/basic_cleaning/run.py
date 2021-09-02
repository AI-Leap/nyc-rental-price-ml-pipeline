#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    logger.info("Downloading artifact")
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    df = pd.read_csv(artifact_local_path)
    min_price = args.min_price
    max_price = args.max_price

    logger.info("Dropping data not between min_price & max_price")
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()

    logger.info("Converting last_review data to datetime")
    df['last_review'] = pd.to_datetime(df['last_review'])

    logger.info("Saving data to csv")
    df.to_csv(args.output_artifact, index=False)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )

    logger.info("Logging artifact")
    artifact.add_file(args.output_artifact)
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="artifact to be cleaned",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="cleaned artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="type of the output",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="output description",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="miniumn price",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="maximum price",
        required=True
    )


    args = parser.parse_args()

    go(args)
