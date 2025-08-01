# -*- coding: utf-8 -*-
"""CODE_FINAL_(1).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zhdPuDJzbSDF91L6NoCRq5E9STMYhCT-
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('dataset3.csv.csv')
df

for col in df.columns:
    print(col)

for col in df.columns:
    min_val = df[col].min()
    max_val = df[col].max()

    if df[col].dtype == 'int64' or df[col].dtype == 'float64':
        print(f"{col} (int): {min_val} to {max_val}")
    elif pd.api.types.is_datetime64_any_dtype(df[col]):
        print(f"{col} (date): {min_val.strftime('%d/%m/%Y')} to {max_val.strftime('%d/%m/%Y')}")
    elif df[col].dtype == 'object':
      unique_vals = df[col].unique()
      print(f"{col}: {unique_vals}")
    else:
        print(f"{col} (other): {min_val} to {max_val}")

df.info()

df.describe()

summary = pd.DataFrame({
    'Mean': df.mean(numeric_only=True),
    'Median': df.median(numeric_only=True),
    'Std': df.std(numeric_only=True),
    'Min': df.min(numeric_only=True),
    'Max': df.max(numeric_only=True)
})
for col in summary.columns:
  if col == 'Mean' or col == 'Std':
    summary[col] = summary[col].round(2)
  else:
    summary[col] = summary[col].round().astype(int)
print(summary)

df.isna().sum()

for col in df.columns:
  print(f"\nColumn: {col}")
  print(df[col].value_counts())

for col in df.columns:
  print(f"\nColumn: {col}")
  print(df[col].unique())

age_order = ["Less than 20", "21 to 35", "36 to 50", "51 or more"]
df["AGE"] = pd.Categorical(df["AGE"], categories=age_order, ordered=True)

plt.figure(figsize=(12, 8))
ax = sns.countplot(data=df, x="AGE", palette="colorblind")
plt.title("Distribution of Age Groups",fontsize=20)
plt.xlabel("Age Group")
plt.ylabel("Count")

# הוספת המספרים מעל כל עמודה
for p in ax.patches:
    count = int(p.get_height())  # גובה העמודה = כמות המופעים
    ax.annotate(f'{count}',
                (p.get_x() + p.get_width() / 2., count),
                ha='center', va='bottom', fontsize=16, color='black')

plt.savefig("age_group_bar_chart.png")
plt.show()
plt.close()

def convert_gender(value):
    if value == 'Male':
        return 1
    elif value == 'Female':
        return 0
    else:
        return value  # מחזיר את הערך המקורי אם הוא שונה

df['GENDER'] = df['GENDER'].apply(convert_gender)

def convert_age(value):
    value = str(value).strip()
    if value == 'Less than 20':
        return 1
    elif value == '21 to 35':
        return 2
    elif value == '36 to 50':
        return 3
    elif value == '51 or more':
        return 4

df['AGE'] = df['AGE'].apply(convert_age)
df

for col in df.columns:
  print(f"{col}: {df[col].dtype}")

df['AGE'] = df['AGE'].astype(int)

df['Timestamp']= pd.to_datetime(df['Timestamp'])
df['Timestamp'] = df['Timestamp'].dt.year

for col in df.columns:
  print(f"{col}: {df[col].dtype}")

df['DAILY_STRESS'] = df['DAILY_STRESS'].replace('1/1/00', 0)
print(df['DAILY_STRESS'].value_counts())
for val in df['DAILY_STRESS'].unique():
    print(f"{val} --- {type(val)}")

# המרת כל העמודה למספרים
df['DAILY_STRESS'] = pd.to_numeric(df['DAILY_STRESS'], errors='coerce')
df['DAILY_STRESS'].fillna(0, inplace=True)


for val in df['DAILY_STRESS'].unique():
    print(f"{val} --- {type(val)}")
print(df['DAILY_STRESS'].value_counts())

for col in df.columns:
  print(f"{col}: {df[col].dtype}")

corr = df.corr(numeric_only=True)
plt.figure(figsize=(15, 12))

heatmap = sns.heatmap(corr,
                      annot=True,
                      fmt=".2f",
                      cmap="viridis",
                      annot_kws={"size": 10})

# הגדלת הטקסט של סרגל הצבע
colorbar = heatmap.collections[0].colorbar
colorbar.ax.tick_params(labelsize=12)  # גודל הכתב של סרגל הצבע

plt.title("Correlation Heatmap", fontsize=24)
plt.xticks(rotation=90, fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("heatmap.png", dpi=100, bbox_inches='tight')
plt.show()

# בוחרים רק עמודות מספריות
df_numeric = df.select_dtypes(include=['number'])

# מסירים את משתנה המטרה
df_numeric = df_numeric.drop('WORK_LIFE_BALANCE_SCORE', axis=1)

# מחשבים את מטריצת הקורלציה
corr_matrix = df_numeric.corr().abs()

# יוצרים רשימת זוגות משתנים עם ערכי הקורלציה ביניהם
corr_pairs = corr_matrix.unstack()

# מסירים קורלציה עצמית (עם עצמו)
corr_pairs = corr_pairs[corr_pairs < 1]

# מסירים כפילויות (כל זוג פעם אחת בלבד)
corr_pairs = corr_pairs.drop_duplicates()

# מוצאים את שני המשתנים עם הקורלציה הגבוהה ביותר
strongest_pair = corr_pairs.sort_values(ascending=False).head(1)

print("The two variables with the highest absolute correlation are:")
print(strongest_pair)

# Create histograms for key numeric variables
import matplotlib.pyplot as plt

key_numeric_vars = ['WORK_LIFE_BALANCE_SCORE', 'DAILY_STRESS', 'SLEEP_HOURS', 'DAILY_STEPS', 'FRUITS_VEGGIES']

plt.figure(figsize=(20, 16))

# עדכון הגדרות כלליות של פונט
plt.rcParams.update({
    'font.size': 18,
    'axes.titlesize': 16,
    'axes.labelsize': 18
})

for i, var in enumerate(key_numeric_vars, 1):
    plt.subplot(3, 2, i)

    # יצירת היסטוגרמה + קבלת הנתונים שלה
    counts, bins, patches = plt.hist(df[var], bins=20, alpha=0.8, color='mediumseagreen', edgecolor='black')
    plt.ylim(0,max(counts)*1.15)

    # הוספת מספרים מעל כל עמודה
    for count, bin_left in zip(counts, bins[:-1]):
        if count > 0:
            plt.text(bin_left + (bins[1]-bins[0])/2, count + max(counts)*0.02, str(int(count)),
         ha='center', fontsize=10.5, color='black')

    plt.title(f'Distribution of {var}', fontweight='normal')
    plt.xlabel(var, fontsize=14)
    plt.ylabel('Frequency', fontsize=16)
    plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('numeric_variables_histograms.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# שם משתנה המטרה
target_variable = 'WORK_LIFE_BALANCE_SCORE'

# חישוב מטריצת מתאם
correlation_matrix = df.corr(numeric_only=True)

# מתאם עם משתנה המטרה
correlation_with_target = correlation_matrix[target_variable].drop(target_variable)

# בחירת ערכים עם מתאם מעל 0.45 או מתחת ל־-0.45
threshold = 0.45
filtered_corr = correlation_with_target[correlation_with_target.abs() >= threshold]

# סידור לפי עוצמת הקשר
top_features = filtered_corr.reindex(filtered_corr.abs().sort_values(ascending=False).index)

# שמירה של 11 משתנים בלבד
top_features = top_features.head(11)

# הדפסת טבלה מסודרת
print("Top 11 Most Informative Features (|r| ≥ 0.45):")
print(top_features)

for i in top_features.index:
  print(i)

selected_features = ['ACHIEVEMENT', 'SUPPORTING_OTHERS', 'TODO_COMPLETED',
                     'PLACES_VISITED', 'TIME_FOR_PASSION', 'CORE_CIRCLE',
                     'PERSONAL_AWARDS', 'FLOW', 'LIVE_VISION',
                     'DONATION', 'FRUITS_VEGGIES']

df_selected = df[selected_features + ['WORK_LIFE_BALANCE_SCORE']]
df_selected

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np

# שלב 1: משתנים
features = ['ACHIEVEMENT', 'SUPPORTING_OTHERS', 'TODO_COMPLETED',
            'PLACES_VISITED', 'TIME_FOR_PASSION', 'CORE_CIRCLE',
            'PERSONAL_AWARDS', 'FLOW', 'LIVE_VISION',
            'DONATION', 'FRUITS_VEGGIES']

X = df[features]
y = df['WORK_LIFE_BALANCE_SCORE']

# שלב 2: חלוקה ל־Train (70%), Validation (15%), Test (15%)
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.15, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.1765, random_state=42)

# שלב 3: סטנדריזציה
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# שלב 4: אימון
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# שלב 5: חיזוי
val_pred = model.predict(X_val_scaled)
test_pred = model.predict(X_test_scaled)

# שלב 6: הדפסת כל המדדים כולל MSE
def print_metrics(name, y_true, y_pred):
    print(f"\n{name} Performance:")
    print(f"R2 Score: {(r2_score(y_true, y_pred)):>7.3f}")
    print(f"MSE:      {(mean_squared_error(y_true, y_pred)):>9.3f}")
    print(f"RMSE:     {(np.sqrt(mean_squared_error(y_true, y_pred))):>8.3f}")
    print(f"MAE:      {(mean_absolute_error(y_true, y_pred)):>8.3f}")

print_metrics("Validation", y_val, val_pred)
print_metrics("Test", y_test, test_pred)

import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
plt.scatter(y_test, test_pred, alpha=0.5, color='blue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel("Actual WORK_LIFE_BALANCE_SCORE")
plt.ylabel("Predicted")
plt.title("Regression Predictions vs. Actual")
plt.grid(True)
plt.legend(['Actual', 'Prediction'])
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# חישוב שיורים (residuals)
residuals = y_test - test_pred

# גרף שיורים מול ערכים חזויים
plt.figure(figsize=(8, 5))
sns.scatterplot(x=test_pred, y=residuals)
plt.axhline(0, color='red', linestyle='--')
plt.title('Residuals vs. Predicted Values')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.grid(True)
plt.savefig('residuals.png', dpi=300, bbox_inches='tight')
plt.show()
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# חישוב שיורים (residuals)
residuals = y_test - test_pred

# חישוב סף חריגים: לדוגמה, 2 סטיות תקן מהשאריות
threshold = 2 * np.std(residuals)

plt.figure(figsize=(8, 5))
sns.scatterplot(x=test_pred, y=residuals)

# סימון נקודות חריגות בצבע אחר ובגודל גדול יותר
outliers_mask = np.abs(residuals) > threshold
sns.scatterplot(x=test_pred[outliers_mask], y=residuals[outliers_mask],
                color='red', s=20, label='Outliers')

plt.axhline(0, color='red', linestyle='--')
plt.title('Residuals vs. Predicted Values with Outliers')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.legend()
plt.grid(True)
plt.savefig('residuals_outliers.png', dpi=300, bbox_inches='tight')
plt.show()
plt.tight_layout()

# טבלת השוואה בין תחזיות, אמת, ושיורים
res_df = pd.DataFrame({
    'Actual': y_test.values,
    'Predicted': test_pred,
    'Residual': residuals
})

# מיון לפי גודל השגיאה המוחלטת
largest_errors = res_df.reindex(res_df['Residual'].abs().sort_values(ascending=False).index)

# הדפסת שתי הדוגמאות הכי שגויות
print("חמש הטעויות הגדולות ביותר:")
print(largest_errors.head(5))

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import numpy as np

# שלב 1: משתנים
features = ['ACHIEVEMENT', 'SUPPORTING_OTHERS', 'TODO_COMPLETED',
            'PLACES_VISITED', 'TIME_FOR_PASSION', 'CORE_CIRCLE',
            'PERSONAL_AWARDS', 'FLOW', 'LIVE_VISION',
            'DONATION', 'FRUITS_VEGGIES']

X = df[features]
y = df['WORK_LIFE_BALANCE_SCORE']

# שלב 2: חלוקה ל־Train (70%), Validation (15%), Test (15%)
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.15, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.1765, random_state=42)

# שלב 3: פייפליין עם סטנדריזציה + רגרסיה לינארית
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('lr', LinearRegression())
])

# שלב 4: הגדרת פרמטרים (אין הרבה היפר-פרמטרים ללינארית, אבל אפשר לבדוק fit_intercept ו־normalize)
param_grid = {
    'lr__fit_intercept': [True, False],
    'lr__positive': [False, True]
}

# שלב 5: GridSearchCV
grid = GridSearchCV(pipe, param_grid, cv=5, scoring='neg_root_mean_squared_error')
grid.fit(X_train, y_train)

# שלב 6: התוצאות
print("Best Parameters:", grid.best_params_)

# ניבוי על סט ה־Validation וה־Test
val_pred = grid.predict(X_val)
test_pred = grid.predict(X_test)

# שלב 7: פונקציית הדפסת מדדים
def print_metrics(name, y_true, y_pred):
    print(f"\n{name} Performance:")
    print(f"R2 Score: {(r2_score(y_true, y_pred)):>7.3f}")
    print(f"MSE:      {(mean_squared_error(y_true, y_pred)):>9.3f}")
    print(f"RMSE:     {(np.sqrt(mean_squared_error(y_true, y_pred))):>8.3f}")
    print(f"MAE:      {(mean_absolute_error(y_true, y_pred)):>8.3f}")

print_metrics("Validation", y_val, val_pred)
print_metrics("Test", y_test, test_pred)

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np
import pandas as pd

# --- שלב 1: משתנים ---
features = ['ACHIEVEMENT', 'SUPPORTING_OTHERS', 'TODO_COMPLETED',
            'PLACES_VISITED', 'TIME_FOR_PASSION', 'CORE_CIRCLE',
            'PERSONAL_AWARDS', 'FLOW', 'LIVE_VISION',
            'DONATION', 'FRUITS_VEGGIES']

X = df[features]
y = df['WORK_LIFE_BALANCE_SCORE']

# --- שלב 2: חלוקה ל־Train (70%), Validation (15%), Test (15%) ---
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.15, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.1765, random_state=42)

# --- שלב 3: סטנדריזציה (לא חובה ל-RF, אבל שומר עקביות) ---
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# --- שלב 4: GridSearchCV רק על Train בלבד! ---
param_grid = {
    'n_estimators': [100],
    'max_depth': [None, 10],
    'min_samples_split': [2]
}

rf = RandomForestRegressor(random_state=42)
grid = GridSearchCV(rf, param_grid, cv=5, scoring='r2', n_jobs=-1)
grid.fit(X_train_scaled, y_train)

best_params_rf = grid.best_params_
best_model_rf = grid.best_estimator_

# --- שלב 5: חיזוי על ולידציה וסט בדיקה ---
val_pred_rf = best_model_rf.predict(X_val_scaled)
test_pred_rf = best_model_rf.predict(X_test_scaled)

# --- שלב 6: הדפסת ביצועים לפי תבנית מסודרת ---
def print_metrics(name, y_true, y_pred):
    print(f"\n{name} Performance:")
    print(f"R2 Score: {(r2_score(y_true, y_pred)):>8.3f}")
    print(f"MSE:      {(mean_squared_error(y_true, y_pred)):>10.3f}")
    print(f"RMSE:     {(np.sqrt(mean_squared_error(y_true, y_pred))):>9.3f}")
    print(f"MAE:      {(mean_absolute_error(y_true, y_pred)):>9.3f}")

# --- שלב 7: תוצאות ---
print(f"\nGridSearchCV Best Parameters: {best_params_rf}")
print_metrics("Validation", y_val, val_pred_rf)
print_metrics("Test", y_test, test_pred_rf)

from scipy.stats import ttest_rel, t
import numpy as np

# --- שגיאות ריבועיות ---
errors_rf = (y_val - val_pred_rf) ** 2
errors_lr = (y_val - val_pred) ** 2

# --- הפרש שגיאות ---
diffs = errors_rf - errors_lr
mean_diff = np.mean(diffs)
std_diff = np.std(diffs, ddof=1)
n = len(diffs)

# --- T-test על השגיאות ---
t_stat, p_value = ttest_rel(errors_rf, errors_lr)

# --- רווח סמך 95% להפרש ---
alpha = 0.05
t_crit = t.ppf(1 - alpha/2, df=n-1)
margin_error = t_crit * (std_diff / np.sqrt(n))
ci_lower = mean_diff - margin_error
ci_upper = mean_diff + margin_error

# --- הדפסות ---
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value (two-tailed): {p_value:.4f}")
print(f"95% Confidence Interval for Mean Error Difference (RF - LR): [{ci_lower:.4f}, {ci_upper:.4f}]")

# --- מסקנה לפי p-value ---
if p_value < 0.05:
    print("✅ קיים הבדל מובהק סטטיסטית בין שגיאות המודלים")
else:
    print("❌ לא נמצא הבדל מובהק סטטיסטית בין המודלים")

import pandas as pd

# הפיצ'רים שנבחרו
selected_features = ['ACHIEVEMENT', 'SUPPORTING_OTHERS', 'TODO_COMPLETED',
                     'PLACES_VISITED', 'TIME_FOR_PASSION', 'CORE_CIRCLE',
                     'PERSONAL_AWARDS', 'FLOW', 'LIVE_VISION',
                     'DONATION', 'FRUITS_VEGGIES']

# יוצרים DataFrame חדש עם הפיצ'רים
df_selected = df[selected_features].copy()

# מוסיפים את משתנה המטרה
df_selected['WORK_LIFE_BALANCE_SCORE'] = df['WORK_LIFE_BALANCE_SCORE']

# בינאריזציה רק למשתנה המטרה לפי מחצית הטווח שלו
min_val = df_selected['WORK_LIFE_BALANCE_SCORE'].min()
max_val = df_selected['WORK_LIFE_BALANCE_SCORE'].max()
threshold = (min_val + max_val) / 2

# יוצרים עמודה בינארית חדשה
df_selected['TARGET_BINARY'] = (df_selected['WORK_LIFE_BALANCE_SCORE'] >= threshold).astype(int)

# אם רוצים, אפשר גם להסיר את העמודה המקורית (לא חובה)
# df_selected = df_selected.drop(columns=['WORK_LIFE_BALANCE_SCORE'])

# תצוגה
df_selected.head()

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# --- 1. הגדרת פיצ'רים ומטרה ---
features = ['ACHIEVEMENT', 'SUPPORTING_OTHERS', 'TODO_COMPLETED',
            'PLACES_VISITED', 'TIME_FOR_PASSION', 'CORE_CIRCLE',
            'PERSONAL_AWARDS', 'FLOW', 'LIVE_VISION',
            'DONATION', 'FRUITS_VEGGIES']

X = df_selected[features]
y = df_selected['TARGET_BINARY']

# --- 2. חלוקה ל־Train (70%), Validation (15%), Test (15%) ---
# שלב ראשון – חילוץ 15% לבדיקה
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

# שלב שני – חילוץ 15/85 ≈ 0.176 לולידציה מתוך מה שנשאר
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.1765, random_state=42)

# --- 3. מודל ואימון על סט האימון בלבד ---
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# --- 4. חיזוי ---
y_val_pred = model.predict(X_val)
y_test_pred = model.predict(X_test)

# --- 5. הערכת ביצועים ---
def print_eval(name, y_true, y_pred):
    print(f"\n{name} Performance:")
    print("Accuracy:", round(accuracy_score(y_true, y_pred), 3))
    print("Classification Report:")
    print(classification_report(y_true, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_true, y_pred))

print_eval("Validation", y_val, y_val_pred)
print_eval("Test", y_test, y_test_pred)

import pandas as pd

# הגדרת עמודת המטרה
y = df_selected['TARGET_BINARY']

# ספירת אפסים ואחדים
counts = y.value_counts()
print("ספירת הערכים בעמודת y (TARGET_BINARY):")
print(counts)

# הדפסת כמות אפסים ואחדים
print(f"\nכמות אפסים (0): {counts[0]}")
print(f"כמות אחדים (1): {counts[1]}")

# בדיקת חוסר איזון
ratio = counts[1] / counts[0]
print(f"\nיחס אחדים לאפסים: {ratio:.2f}")
if ratio < 0.5 or ratio > 2:
    print("⚠️ יש חוסר איזון בין הקבוצות.")
else:
    print("✔️ אין חוסר איזון משמעותי.")

from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# --- 1. הגדרת פיצ'רים ומטרה ---
features = ['ACHIEVEMENT', 'SUPPORTING_OTHERS', 'TODO_COMPLETED',
            'PLACES_VISITED', 'TIME_FOR_PASSION', 'CORE_CIRCLE',
            'PERSONAL_AWARDS', 'FLOW', 'LIVE_VISION',
            'DONATION', 'FRUITS_VEGGIES']

X = df_selected[features]
y = df_selected['TARGET_BINARY']

# --- 2. חלוקה ל-Train (70%), Validation (15%), Test (15%) ---

# שלב ראשון: נפריד 15% לבדיקה
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

# שלב שני: מתוך ה־85% שנותרו, נוציא 15% נוספים לוולידציה ← 15/85 ≈ 0.1765
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.1765, random_state=42)

# --- 3. יצירת והכשרת המודל על סט האימון בלבד ---
model = XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)

# --- 4. חיזוי על סט הוולידציה והבדיקה ---
y_val_pred = model.predict(X_val)
y_test_pred = model.predict(X_test)

# --- 5. הערכת המודל ---
def print_results(name, y_true, y_pred):
    print(f"\n{name} Performance:")
    print("Accuracy:", accuracy_score(y_true, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_true, y_pred))

# --- 6. הדפסת ביצועים ---
print_results("Validation", y_val, y_val_pred)
print_results("Test", y_test, y_test_pred)

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pandas as pd

# --- 1. הגדרת פיצ'רים ומטרה ---
features = ['ACHIEVEMENT', 'SUPPORTING_OTHERS', 'TODO_COMPLETED',
            'PLACES_VISITED', 'TIME_FOR_PASSION', 'CORE_CIRCLE',
            'PERSONAL_AWARDS', 'FLOW', 'LIVE_VISION',
            'DONATION', 'FRUITS_VEGGIES']

X = df_selected[features]
y = df_selected['TARGET_BINARY']  # משתנה מטרה בינארי בלבד

# --- 2. חלוקה ל־Train (70%), Validation (15%), Test (15%) ---
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.15, random_state=42, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.1765, random_state=42, stratify=y_temp)

# --- 3. GridSearchCV על סט האימון בלבד ---
param_grid = {
    'n_estimators': [100],
    'max_depth': [None, 10],
    'min_samples_split': [2]
}

clf = RandomForestClassifier(random_state=42)
grid = GridSearchCV(clf, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid.fit(X_train, y_train)

best_model = grid.best_estimator_
best_params = grid.best_params_

# --- 4. חיזוי ---
val_pred = best_model.predict(X_val)
test_pred = best_model.predict(X_test)

# --- 5. הדפסת תוצאות ---
def print_classification_metrics(name, y_true, y_pred):
    print(f"\n{name} Performance:")
    print(f"Accuracy:     {accuracy_score(y_true, y_pred):.3f}")
    print("Classification Report:")
    print(classification_report(y_true, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_true, y_pred))

print(f"\nGridSearchCV Best Parameters: {best_params}")
print_classification_metrics("Validation", y_val, val_pred)
print_classification_metrics("Test", y_test, test_pred)

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# נניח שכבר יש לך את המודל הטוב ביותר:
best_model = grid.best_estimator_

# חיזוי על סט ה־Validation ו־Test
y_val_pred = best_model.predict(X_val)
y_test_pred = best_model.predict(X_test)

# 1. Confusion Matrix עבור סט Validation
cm_val = confusion_matrix(y_val, y_val_pred)
disp_val = ConfusionMatrixDisplay(confusion_matrix=cm_val, display_labels=best_model.classes_)
disp_val.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix - Validation Set")
plt.savefig('confusion_matrix_validation.png', dpi=300, bbox_inches='tight')  # שומרים את התמונה
plt.show()  # מציגים את הגרף

# 2. Confusion Matrix עבור סט Test
cm_test = confusion_matrix(y_test, y_test_pred)
disp_test = ConfusionMatrixDisplay(confusion_matrix=cm_test, display_labels=best_model.classes_)
disp_test.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix - Test Set")
plt.savefig('confusion_matrix_test.png', dpi=300, bbox_inches='tight')  # שומרים את התמונה
plt.show()  # מציגים את הגרף

import numpy as np
import pandas as pd

# --- 1. חיזוי ---
y_val_pred = best_model.predict(X_val)

# --- 2. זיהוי False Positives ו־False Negatives ---
fp_indices = (y_val == 0) & (y_val_pred == 1)  # חזה בטעות 1
fn_indices = (y_val == 1) & (y_val_pred == 0)  # חזה בטעות 0
# --- 3. ספירת טעויות ---
num_fp = fp_indices.sum()
num_fn = fn_indices.sum()

print(f"\nFalse Positives (חזה בטעות 1): {num_fp}")
print(f"False Negatives (חזה בטעות 0): {num_fn}")

# --- 4. הצגת 2 דוגמאות מכל סוג טעות ---
print("\nFalse Positives (חזה בטעות אחד):")
display(X_val[fp_indices].head(2))

print("\nFalse Negatives (חזה בטעות אפס):")
display(X_val[fn_indices].head(2))

from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import pandas as pd

# --- 1. הגדרת פיצ'רים ומטרה ---
features = ['ACHIEVEMENT', 'SUPPORTING_OTHERS', 'TODO_COMPLETED',
            'PLACES_VISITED', 'TIME_FOR_PASSION', 'CORE_CIRCLE',
            'PERSONAL_AWARDS', 'FLOW', 'LIVE_VISION',
            'DONATION', 'FRUITS_VEGGIES']

X = df_selected[features]
y = df_selected['TARGET_BINARY']

# --- 2. חלוקה ל־Train (70%), Validation (15%), Test (15%) ---
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.15, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.1765, random_state=42)

# --- 3. טווח היפרפרמטרים ל־GridSearchCV ---
param_grid = {
    'n_estimators': [100],
    'max_depth': [None, 10]
}

# --- 4. יצירת המודל מסוג XGBClassifier ---
xgb_model = XGBClassifier(
    random_state=42,
    use_label_encoder=False,
    eval_metric='logloss'
)

grid = GridSearchCV(xgb_model, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid.fit(X_train, y_train)

# --- 5. חיזוי ---
best_model = grid.best_estimator_
y_val_pred = best_model.predict(X_val)
y_test_pred = best_model.predict(X_test)

# --- 6. פונקציית הדפסת ביצועים ---
def print_results(name, y_true, y_pred):
    print(f"\n{name} Performance:")
    print("Accuracy:", accuracy_score(y_true, y_pred))
    print("Classification Report:\n", classification_report(y_true, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_true, y_pred))

# --- 7. תוצאות ---
print(f"Best Parameters from GridSearchCV: {grid.best_params_}")
print_results("Validation", y_val, y_val_pred)
print_results("Test", y_test, y_test_pred)

import numpy as np
from statsmodels.stats.contingency_tables import mcnemar
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# נבדוק מתי כל מודל צדק
rf_correct = (y_val == val_pred)
xgb_correct = (y_val == y_val_pred)

a = np.sum(rf_correct & xgb_correct)
b = np.sum(rf_correct & ~xgb_correct)
c = np.sum(~rf_correct & xgb_correct)
d = np.sum(~rf_correct & ~xgb_correct)

table = [[a, b], [c, d]]
print("Contingency Table for McNemar's Test:")
print(np.array(table))

# --- 2. מבחן McNemar ---
result = mcnemar(table, exact=True)
p_value = result.pvalue

print(f"\nMcNemar test p-value (RF vs XGBoost): {p_value:.4f}")
if p_value < 0.05:
    print("✅ ההבדל בין המודלים מובהק סטטיסטית")
else:
    print("⚠️ אין הבדל מובהק סטטיסטית בין המודלים")

# --- 3. Bootstrap 95% אינטרוול סמך להפרש ב-Accuracy ---
n_iterations = 1000
acc_diffs = []

# ודא שהנתונים הם מערכי numpy לטובת דגימת Bootstrap
y_val_array = y_val.to_numpy() if isinstance(y_val, pd.Series) else np.array(y_val)
rf_preds_array = np.array(val_pred)
xgb_preds_array = np.array(y_val_pred)

for _ in range(n_iterations):
    indices = np.random.choice(len(y_val_array), size=len(y_val_array), replace=True)
    acc_rf = accuracy_score(y_val_array[indices], rf_preds_array[indices])
    acc_xgb = accuracy_score(y_val_array[indices], xgb_preds_array[indices])
    acc_diffs.append(acc_rf - acc_xgb)

# חישוב ממוצע הפרש הדיוקים
mean_diff = np.mean(acc_diffs)

# חישוב רווח סמך
ci_lower = np.percentile(acc_diffs, 2.5)
ci_upper = np.percentile(acc_diffs, 97.5)

print(f"\nרווח סמך ברמת 95% להפרש בדיוק בין שני המודלים (RF - XGBoost): [{ci_lower:.4f}, {ci_upper:.4f}]")
print(f"ממוצע הפרש הדיוקים (RF - XGBoost): {mean_diff:.4f}")

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# נניח שכבר יש לך את המודל הטוב ביותר:
best_model = grid.best_estimator_

# חיזוי על סט ה־Validation ו־Test
y_val_pred = best_model.predict(X_val)
y_test_pred = best_model.predict(X_test)

# 1. Confusion Matrix עבור סט Validation
cm_val = confusion_matrix(y_val, y_val_pred)
disp_val = ConfusionMatrixDisplay(confusion_matrix=cm_val, display_labels=best_model.classes_)
disp_val.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix - Validation Set")
plt.savefig('confusion_matrix_validation.png', dpi=300, bbox_inches='tight')  # שומרים את התמונה
plt.show()  # מציגים את הגרף

# 2. Confusion Matrix עבור סט Test
cm_test = confusion_matrix(y_test, y_test_pred)
disp_test = ConfusionMatrixDisplay(confusion_matrix=cm_test, display_labels=best_model.classes_)
disp_test.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix - Test Set")
plt.savefig('confusion_matrix_test.png', dpi=300, bbox_inches='tight')  # שומרים את התמונה
plt.show()  # מציגים את הגרף

import numpy as np
import pandas as pd

# --- 1. חיזוי ---
y_val_pred = best_model.predict(X_val)

# --- 2. זיהוי False Positives ו־False Negatives ---
fp_indices = (y_val == 0) & (y_val_pred == 1)  # חזה בטעות 1
fn_indices = (y_val == 1) & (y_val_pred == 0)  # חזה בטעות 0
# --- 3. ספירת טעויות ---
num_fp = fp_indices.sum()
num_fn = fn_indices.sum()

print(f"\nFalse Positives (חזה בטעות 1): {num_fp}")
print(f"False Negatives (חזה בטעות 0): {num_fn}")

# --- 4. הצגת 2 דוגמאות מכל סוג טעות ---
print("\nFalse Positives (חזה בטעות אחד):")
display(X_val[fp_indices].head(2))

print("\nFalse Negatives (חזה בטעות אפס):")
display(X_val[fn_indices].head(2))