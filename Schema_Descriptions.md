
---
# Model Card Schema Descriptions
### Model Card Documentation

This documentation details the required and optional fields for configuring a `ModelCard`. The variables specified here represent essential information about the model, its usage, and its metadata. Fields like `bias_analysis`, `xai_analysis`, `id`, and `model_requirements` are managed automatically by the system and do not require user input.

| Field Name           | Type              | Description                                                               | Constraints/Example Values                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|----------------------|-------------------|---------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `name`               | `str`             | **Required**. The name of the model card.                                 | Example: `"Model Card for Sentiment Analysis"`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `version`            | `str`             | **Required**. The version of the model card.                              | Example: `"1.0.0"`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `short_description`  | `str`             | **Required**. A brief description of the model card.                      | Example: `"This model detects sentiment in text data."`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `full_description`   | `str`             | **Required**. A comprehensive description of the model card.              | Example: `"This model performs sentiment analysis using NLP techniques and is trained on customer feedback data."`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `keywords`           | `str`             | **Required**. Keywords associated with the model card.                    | Example: `"sentiment analysis, NLP, text classification"`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `author`             | `str`             | **Required**. Author or creator of the model card.                        | Example: `"Jane Doe"`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `input_type`         | `str`             | **Required**. Type of input data accepted by the model.                   | Example: `"text, image, tabular"`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `category`           | `str`             | **Required**. Model category from predefined types.                       | Enum: `"classification", "regression", "clustering", "anomaly detection", "dimensionality reduction", "reinforcement learning", "natural language processing", "computer vision", "recommendation systems", "time series forecasting", "graph learning", "graph neural networks", "generative modeling", "transfer learning", "self-supervised learning", "semi-supervised learning", "unsupervised learning", "causal inference", "multi-task learning", "metric learning", "density estimation", "multi-label classification", "ranking", "structured prediction", "neural architecture search", "sequence modeling", "embedding learning", "other"` |
| `input_data`         | `str`             | **Required**. URL or DOI for the input data.                              | Must be a valid URL, DOI, or empty string.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `output_data`        | `str`             | **Required**. URL or DOI for the output data.                             | Must be a valid URL, DOI, or empty string.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **Optional Fields**  |       |                                                                       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `foundational_model` | `str`             | **Optional**. Foundational model ID or URL if applicable.                 | Example: `"https://huggingface.co/docs/transformers/en/model_doc/flan-t5"`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `documentation`      | `str`             | **Optional**. URL link to documentation for the model.                    | Example: `"https://docs.example.com/modeldocs.md"`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |



### AI Model Documentation

This documentation details the fields required to configure an `AIModel`, representing the essential metadata for the underlying AI model within a `ModelCard`.

| Field Name           | Type              | Description                                                                                                          | Constraints/Example Values                                                                                    |
|----------------------|-------------------|----------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| `name`               | `str`             | **Required**. The name of the AI model.                                                                              | Example: `"Sentiment Analysis Model"`.                                                                        |
| `version`            | `str`             | **Required**. The version of the AI model.                                                                           | Example: `"1.0.0"`.                                                                                           |
| `description`        | `str`             | **Required**. A description of the AI model’s functionality and purpose.                                             | Example: `"This model is trained to detect sentiment in customer feedback."`                                  |
| `owner`              | `str`             | **Required**. The individual or organization that owns the model.                                                    | Example: `"Jane Doe"`.                                                                                        |
| `location`           | `str`             | **Required**. Downloadable URL of the model.                                                                         | Example: `"https://modelrepository.com/model/123"`.                                                           |
| `license`            | `str`             | **Required**. License type for the model usage.                                                                      | Example: `"Apache-2.0"`.                                                                                      |
| `framework`          | `str`             | **Required**. Framework used for developing the model.                                                               | Enum: `"sklearn", "tensorflow", "pytorch", "other"`.                                                          |
| `model_type`         | `str`             | **Required**. Type of AI model structure.                                                                            | Enum: `"cnn", "decision_tree", "dnn", "rnn", "svm", "kmeans", "llm", "random_forest", "lstm", "gnn", "other"` |
| `test_accuracy`      | `float`           | **Required**. Accuracy of the model on test data.                                                                    | Example: `0.89`.                                                                                              |
| **Optional Fields**  |                   |                                                                                                                      |                                                                                                               |
| `model_structure`    | `object`          | **Optional**. Structure of the model in JSON format.                                                                 | Example: `{"layers": [{"type": "Conv2D", "filters": 32}]}`.                                                   |
| `metrics`            | `dict`            | **Optional**. Dictionary of performance metrics for the model. Use `ai_model.add_metric(key, value)` to add metrics. | Example: `ai_model.add_metric("Test loss", loss)`                                                                                                     |


You can validate the model card contents against this schema to ensure that all required fields are present using the following command:
```python
mc.validate()
```

---
