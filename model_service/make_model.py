import pandas as pd
from os import path, getcwd
import joblib
import category_encoders as ce
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv(path.join(getcwd(), 'model', "titanic.csv"))
df['Age']= df['Age'].fillna(df['Age'].mean())
df.dropna(subset=['Embarked'],inplace=True)
y = pd.Series(df['Survived'])
drop_list = ['Survived','Name','Ticket','Cabin']
X = df.drop(drop_list,axis=1)
encoder=ce.OneHotEncoder(handle_unknown='return_nan',return_df=True,use_cat_names=True)
X = encoder.fit_transform(X)
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,stratify=y,random_state=42)
model = RandomForestClassifier()
model.fit(X_train,y_train)
joblib.dump(model,path.join(getcwd(), 'model', "model_joblib"))
