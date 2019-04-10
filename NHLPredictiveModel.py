import pandas as pd
import numpy as np
import sklearn
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, roc_curve, auc
import statsmodels.api as sm
from NHLScrape import NHLGames, NHLStandings
# import matplotlib.pyplot as plt


def home_team_PK(row):
    home_team = row["Home"]
    home_PK = ladder.loc[home_team]["PK%"]
    return float(home_PK)


def visitor_team_PK(row):
    visitor_team = row["Visitor"]
    visitor_PK = ladder.loc[visitor_team]["PK%"]
    return float(visitor_PK)


def home_team_PP(row):
    home_team = row["Home"]
    home_PP = ladder.loc[home_team]["PP%"]
    return float(home_PP)


def home_team_SCF(row):
    home_team = row["Home"]
    home_SCF = ladder.loc[home_team]["SCF%"]
    return float(home_SCF)


def visitor_team_SCF(row):
    visitor_team = row["Visitor"]
    visitor_SCF = ladder.loc[visitor_team]["SCF%"]
    return float(visitor_SCF)


def visitor_team_axdiff(row):
    visitor_team = row["Visitor"]
    visitor_axdiff = ladder.loc[visitor_team]["axDiff"]
    return int(visitor_axdiff)


ladder = NHLStandings(2018)
results = NHLGames(2019)
results.set_index('Date')

results['HomeWin'] = results['HomeWin'].astype(int)
results['HomeTeamSCF%'] = results.apply(home_team_SCF, axis=1)
results['VisitorTeamSCF%'] = results.apply(visitor_team_SCF, axis=1)
results['VisitorTeamPK%'] = results.apply(visitor_team_PK, axis=1)
results['VisitorTeamAxDiff'] = results.apply(visitor_team_axdiff, axis=1)
results['HomeTeamPP%'] = results.apply(home_team_PP, axis=1)

results = sklearn.utils.shuffle(results, random_state=26)
X = results.drop(["HomeWin", "Date", "Home", "Visitor",
                  "Home Goals", "Visitor Goals"], axis=1).values
y = results['HomeWin'].values

encoder = LabelEncoder()
encoder.fit(y)
y = encoder.transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    StandardScaler().fit_transform(X), y, test_size=0.20, random_state=14)
results

kfold = KFold(n_splits=10, random_state=14)
clf = LogisticRegressionCV(cv=kfold, random_state=14)
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
accuracy = clf.score(X_test, y_test)

X2 = sm.add_constant(X)
est = sm.Logit(y, X2)
est2 = est.fit()
print(est2.summary())
print(classification_report(y_test, predictions))
print(f'Model Accuracy: {round(accuracy, 4) * 100}%')

# fpr, tpr, threshold = roc_curve(y_test, predictions)
# roc_auc = auc(fpr, tpr)
# plt.title('Receiver Operating Characteristic')
# plt.plot(fpr, tpr, 'b', label='AUC = %0.2f' % roc_auc)
# plt.legend(loc='lower right')
# plt.plot([0, 1], [0, 1], 'r--')
# plt.xlim([0, 1])
# plt.ylim([0, 1])
# plt.ylabel('True Positive Rate')
# plt.xlabel('False Positive Rate')
# plt.show()
