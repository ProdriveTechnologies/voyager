import os
import sys
import argparse
import json

if __name__ == "__main__":
    print("Deployment tool")

    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('location')

    args = parser.parse_args()

    spec = {
        "files": [
            {
                "pattern": "nop.txt",
                "target": args.location,
                "props": "installer.enable;"
            }
        ]
    }

    custom_build = os.environ.get('bamboo_customRevision')
    if custom_build != None:
        print("Releasing {} @ {}".format(args.file, custom_build))
        spec['files'][0]['pattern'] = args.file
        spec['files'][0]['target'] = args.location.replace('<tag_version>', custom_build)
    else:
        print("No custom build was found. releasing nothing")

    print('Deploying spec: ')
    print(json.dumps(spec, indent=2))

    with open('artifactory_spec.json', 'w') as outfile:
        json.dump(spec, outfile, indent=2)
