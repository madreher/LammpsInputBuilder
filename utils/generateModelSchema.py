import json
from lammpsinputbuilder.model.workflow_builder_model import WorkflowBuilderModel

def main():
    model_schema = WorkflowBuilderModel.model_json_schema()
    print(json.dumps(model_schema, indent=4))

if __name__ == "__main__":
    main()