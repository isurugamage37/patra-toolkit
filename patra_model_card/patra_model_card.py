from dataclasses import dataclass, field
from typing import List, Optional, Callable, Dict
from dataclasses import dataclass
import json
from json import JSONEncoder
from jsonschema import validate
import os.path
from patra_model_card.fairlearn_bias import BiasAnalyzer
from patra_model_card.shap_xai import ExplainabilityAnalyser
import pkg_resources
import requests
import jsonschema

SCHEMA_JSON = os.path.join(os.path.dirname(__file__), 'schema', 'schema.json')

@dataclass
class Metric:
    key: str
    value: str



@dataclass
class AIModel:
    name: str
    version: str
    description: str
    owner: str
    location: str
    license: str
    framework: str
    model_type: str
    test_accuracy: float
    model_structure: Optional[object] = field(default_factory=dict)
    metrics: Dict[str, str] = field(default_factory=dict)

    def add_metric(self, key: str, value: str) -> None:
        self.metrics[key] = value

    def remove_nulls(self, model_structure):
        """
        Cleans the model structure by removing the null values.
        :param model_structure:
        :return:
        """
        if isinstance(model_structure, dict):
            return {k: self.remove_nulls(v) for k, v in model_structure.items() if v is not None and self.remove_nulls(v)}
        elif isinstance(model_structure, list):
            return [self.remove_nulls(v) for v in model_structure if v is not None and self.remove_nulls(v) != []]
        else:
            return model_structure

    def populate_model_structure(self, trained_model):
        """
        Populates model structure based on trained model and framework.
        :param trained_model:
        :param framework:
        :return:
        """
        if self.framework is not None and self.framework == 'tensorflow':
            json_structure = json.loads(trained_model.to_json())
            cleaned_structure = self.remove_nulls(json_structure)
            self.model_structure = cleaned_structure
        else:
            self.model_structure = {}


@dataclass
class BiasAnalysis:
    demographic_parity_difference: float
    equal_odds_difference: float

@dataclass
class ExplainabilityAnalysis:
    name: str
    metrics: List[Metric] = field(default_factory=list)


@dataclass
class ModelCard:
    name: str
    version: str
    short_description: str
    full_description: str
    keywords: str
    author: str
    input_type: str
    category: str
    input_type: str
    input_data: Optional[str] = ""
    output_data: Optional[str] = ""
    foundational_model: Optional[str] = ""
    ai_model: Optional[AIModel] = None
    bias_analysis: Optional[BiasAnalysis] = None
    xai_analysis: Optional[ExplainabilityAnalysis] = None
    model_requirements: Optional[List] = None

    def __str__(self):
        """
        Overriding the __str__ to pretty print the model card in Json format.
        :return:
        """
        return json.dumps(self.__dict__, cls=ModelCardJSONEncoder, indent=4, separators=(',', ': '))

    def populate_bias(self, dataset, true_labels, predicted_labels, sensitive_feature_name, sensitive_feature_data, model):
        """
        Calculates the fairness metrics and adds it to the model card.
        :param dataset:
        :param true_labels:
        :param predicted_labels:
        :param sensitive_feature_name:
        :param sensitive_feature_data:
        :param model:
        :return:
        """
        bias_analyzer = BiasAnalyzer(dataset, true_labels, predicted_labels, sensitive_feature_name,
                                          sensitive_feature_data, model)

        self.bias_analysis = bias_analyzer.calculate_bias_metrics()

    def populate_xai(self, train_dataset, column_names, model, n_features=10):
        """
        Calculates the top n_features in terms of feature importance and add's it to the model card.
        :param train_dataset:
        :param column_names:
        :param model:
        :param n_features:
        :return:
        """
        xai_analyzer = ExplainabilityAnalyser(train_dataset, column_names, model)
        self.xai_analysis = xai_analyzer.calculate_xai_features(n_features)

    def populate_requirements(self):
        """
        gets all the package requirements for this model.
        :return:
        """
        # Patra related packages. Remove this from the requirement list.
        exclude_packages = {"shap", "fairlearn"}

        # Get all the installed packages
        installed_packages = pkg_resources.working_set
        packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])

        # all packages except Patra packages
        filtered_packages_list = [pkg for pkg in packages_list if pkg.split("==")[0] not in exclude_packages]
        self.model_requirements = filtered_packages_list

    def validate(self):
        """
        Validates the current model against the Model Card schema
        :return:
        """
        # Convert the dataclass object to JSON string using the custom encoder
        mc_json = self.__str__()

        try:
            with open(SCHEMA_JSON, 'r') as schema_file:
                schema = json.load(schema_file)
            jsonschema.validate(instance=json.loads(mc_json), schema=schema)
            return True
        except jsonschema.ValidationError as e:
            # Print the error message only
            print(e.message)  # This will print only the specific error message
            return False
        except Exception as e:
            # For any other exception, print the error message
            print(f"An unexpected error occurred: {e}")
            return False

    def submit(self, patra_server_url):
        """
        Validates and submits the model card to the Patra Server.
        :param patra_server_url:
        """
        if self.validate():
            try:
                headers = {'Content-Type': 'application/json'}  # Set the content type to JSON
                response = requests.post(patra_server_url, json=json.loads(str(self)), headers=headers)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                return None


    def save(self, file_location):
        """
        Saves the model card as a json file.
        """
        with open(file_location, 'w') as json_file:
            json_file.write(str(self))


class ModelCardJSONEncoder(JSONEncoder):
    """
    JSON encoder for the model card.
    """
    def default(self, obj):
        if isinstance(obj, (ModelCard, Metric, AIModel, ExplainabilityAnalysis, BiasAnalysis)):
            return obj.__dict__
        return super().default(obj)

