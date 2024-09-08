#!/usr/bin/env python3

import json
import argparse

import numpy as np


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--projectPath", type=str, dest="inputFile", required=True, help="Path to a Radahn project")
    args = parser.parse_args()

    with open(args.inputFile) as f:
        data = json.load(f)

        if "header" not in data:
            raise RuntimeError("No header in JSON file, unable to determine the format of the json file.")


        if "format" not in data["header"]:
            raise RuntimeError("No format in JSON file, unable to determine the format of the json file.")
        

        if data["header"]["format"] != "radahn":
            raise RuntimeError(f"Unsupported format {data['header']['format']}")

        # Check if there are anchors 
        if "anchors" in data:
            for anchorName in data["anchors"].keys():
                if "atomIndexes" not in data["anchors"][anchorName]:
                    raise RuntimeError(f"Anchor {anchorName} has no atomIndexes")
                selections = data["anchors"][anchorName]["atomIndexes"]
                npSelection = np.array(selections)
                npSelection += 1

                print(f"{anchorName} {npSelection}")

        if "selections" in data:
            for selectionName in data["selections"].keys():
                if "atomIndexes" not in data["selections"][selectionName]:
                    raise RuntimeError(f"Selection {selectionName} has no atomIndexes")
                selections = data["selections"][selectionName]["atomIndexes"]
                npSelection = np.array(selections)
                npSelection += 1

                print(f"{selectionName} {npSelection}")

        if "thermostats" in data:
            for thermostatName in data["thermostats"].keys():
                if "atomIndexes" not in data["thermostats"][thermostatName]:
                    raise RuntimeError(f"Thermostat {thermostatName} has no atomIndexes")
                selections = data["thermostats"][thermostatName]["atomIndexes"]
                npSelection = np.array(selections)
                npSelection += 1

                print(f"{thermostatName} {npSelection}")

    print("Done")

if __name__ == "__main__":
    main()