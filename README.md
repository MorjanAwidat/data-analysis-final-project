Final Report & GitHub Submission Assignment (5)

Conclusion:


The goal of this study was to examine which lifestyle characteristics most significantly impact an individual’s quality of life, as measured by the work-life balance score. The dataset consisted of 15,972 observations and initially included 24 features. We adopted a mixed-methods approach both quantitative and qualitative to analyze the data. Categorical features, such as gender and age group, were encoded into numerical values using appropriate encoding techniques.
It is important to note that the dataset did not contain any missing values, and therefore no handling of Nan values or imputation was necessary.
Once all features were numeric, we calculated their correlation with the target variable. To reduce dimensionality and focus on the most relevant variables, we selected 11 features with a Pearson correlation coefficient of 0.45 or higher. These features formed the basis for our predictive modeling. For regression tasks, we applied standardization to the selected features, and for classification tasks, we binarized the target variable into 0 and 1.
We trained four machine learning models: two for regression - Linear Regression and Random Forest Regressor, and two for classification - XGBoost Classifier and Random Forest Classifier. The dataset was split into three subsets: training (70%), validation (15%), and testing (15%). After the initial evaluation, we applied hyperparameter tuning using cross-validation to optimize model performance.
In the regression task, Linear Regression achieved the best results, with an R² of 0.824 and MAE of 15.13. The Random Forest Regressor performed slightly worse (R² = 0.814, MAE = 15.50). A statistically significant difference was found between the two regression models.
In the classification task, Random Forest Classifier achieved the best overall performance, with an accuracy of 0.885 and F1-score of 0.89, as well as strong recall and precision values. The XGBoost Classifier also performed well (accuracy: 0.871, F1: 0.87), but did not outperform the Random Forest model. A statistically significant difference was also found between the two classification models.
An analysis of the class distribution in the classification task showed no significant class imbalance: 5,682 observations were labeled as 0 and 10,290 as 1, yielding a ratio of 1.81. Therefore, no special treatment for class imbalance was required.
These findings offer valuable insights into how personal lifestyle habits influence work-life balance, with practical implications for individuals, organizations, and public health policy.




Limitations:
Despite the strong performance of the models we developed, this project includes several key limitations that should be acknowledged:
1. Model Complexity and Interpretability:
The classification model with the best performance was the Random Forest Classifier, which is based on numerous decision trees. Although highly accurate, its decision-making process lacks transparency.
For example, when the model predicts that an individual has a good work-life balance, it is difficult to identify which features led to that outcome unlike a linear regression model, where each feature's influence is clearly shown.
This lack of explainability may limit the practical use of the model in fields where transparency, trust, or interpretability are essential, such as healthcare, human resources, or personal well-being.
Future work could include interpretability tools such as SHAP or LIME to better understand feature contributions.
2. Failure to Capture Non-Linear Relationships and Interactions in Regression:
The main regression model used in this project was Linear Regression, which assumes independent and linear relationships between features and the target variable. However, in reality, lifestyle factors influence quality of life in more complex, non-linear, and interdependent ways.
This limitation was evident in specific failure cases (observations 9338 and 10914), where large prediction errors occurred, possibly due to the model’s inability to handle unique feature combinations or outliers.
In future projects, non-linear models or robust regression methods (such as Huber Regression) could be explored, as well as adding polynomial or interaction terms.
3. Bias Toward Dominant Features in Classification:
Error analysis revealed that the classification model especially the Random Forest tends to over-rely on specific features such as PERSONAL_AWARDS and FLOW, even when other important indicators (such as TIME_FOR_PASSION or LIVE_VISION) are low.
This led to misclassifications in borderline cases, where some features were high while others were low.
More balanced feature weighting or advanced feature engineering may help reduce this bias and improve the model’s ability to interpret complex profiles.
4. Lack of Feature Interaction Modeling:
Feature selection was based on correlation with the target variable, but a high correlation does not necessarily indicate predictive value.
Moreover, the models did not include interactions between features situations where the effect of one variable depends on another. For example, “sense of purpose” may influence work-life balance more when combined with “free time.”
The absence of such combinations may reduce the model's ability to detect deeper behavioral patterns.
Future models could include engineered interaction features or use algorithms that capture such effects automatically (Gradient Boosting or Neural Networks).


5. Data Quality and Limited Population Representation:
Although the dataset was complete and contained no missing values, there are still important limitations related to data quality. First, all data came from a single source and time period, which may mean it does not fully represent the diversity of populations, cultures, or time-based variations.
For example, the lifestyle of young adults in one country may differ significantly from that of older adults in another but these differences may not be reflected in the dataset.
Additionally, unique or rare lifestyle profiles may have been underrepresented in the training set, making it harder for the model to generalize to such individuals.
Furthermore, several variables in the dataset are based on self-reported questionnaires, which are inherently subjective and may include perceptual bias affecting prediction quality.
Future work could improve data quality by integrating multiple data sources, using longitudinal data collection, or segmenting populations for more tailored analysis.

Future Work:
Building on our findings and the limitations identified, several concrete directions can be pursued to deepen and extend this research:
 .1Enhance Data Diversity and Quality:
Integrate Multiple Data Sources: Collect additional lifestyle and well-being data from different regions, age groups, and cultural contexts to improve representativeness and generalisability.
Longitudinal Data Collection: Design a follow-up survey to capture changes in work-life balance over time, enabling analysis of causal dynamics rather than cross-sectional correlations.
 .2Develop and Evaluate Non-Linear and Interaction-Aware Models:
Advanced Algorithms: Experiment with models capable of capturing non-linear relationships and feature interactions, such as Gradient Boosting Machines, Neural Networks, or Support Vector Regression.
Feature Engineering for Interactions: Create engineered features representing key interactions (“sense of purpose” × “free time”) to explicitly test their predictive utility in both regression and classification tasks.
 .3Improve Model Interpretability and Fairness:
Interpretability Tools: Integrate SHAP, LIME, or other explainability frameworks to quantify each feature’s contribution and flag potential biases in individual predictions.
Fairness Audits: Conduct subgroup analyses (by gender, age, income) to assess whether model performance differs across demographic groups, and apply fairness-enhancing techniques (reweighting, adversarial debiasing) as needed.


4. Enhancing Model Robustness to Outliers and Rare Profiles
Robust Regression Techniques: 
Future work could explore the use of models such as Huber Regression or RANSAC, as well as outlier detection methods like Isolation Forest, to reduce the influence of extreme observations on model performance.
Rare Profile Enrichment: 
In cases where certain population groups are underrepresented in the training data for example, individuals with unique lifestyle combinations the model may fail to learn effectively from them and produce inaccurate predictions.
To address this imbalance, synthetic data generation techniques such as SMOTE (Synthetic Minority Over-sampling Technique) can be applied.
SMOTE creates new synthetic samples based on existing rare examples, allowing for a more balanced training set and improving the model's ability to learn from and generalize to uncommon or atypical profiles.
5. Real-World Implementation and Impact Evaluation:
Development of an Interactive Dashboard:
As part of the model’s practical potential, an interactive dashboard can be developed to allow individual users or HR professionals to input personal lifestyle data such as average sleep hours, time for hobbies, sense of purpose, physical activity, and more and receive a personalized prediction of their Work-Life Balance Score, along with tailored recommendations for improvement.
Such an interface would transform the model’s output into a practical and user-friendly tool that can promote awareness, guide decision-making, and support both individual and organizational well-being. This type of implementation bridges the gap between the research model and real-world applications, enabling measurable impact on users’ daily lives.
A/B Testing in Workplace Settings: 
It is recommended to conduct a controlled pilot within a small organization, where participants are randomly divided into two groups:
One group receives personalized recommendations based on model predictions.
The other group receives no intervention.
After a set period, the two groups can be compared on various well-being indicators such as satisfaction, perceived balance, stress levels, or productivity.
The goal of this testing is to assess whether the model’s real-life use leads to measurable improvements in work-life balance, beyond its statistical performance on data. If results are positive, this would support broader deployment of the model in organizational or personal wellness settings.



