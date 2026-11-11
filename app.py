import streamlit as st
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
st.set_page_config(page_title='Health Risk Explorer',page_icon='🩺',layout='wide')
st.title('🩺 Health Risk Prediction Explorer')
st.caption('Educational classification example. It does not diagnose disease.')
df=pd.read_csv(Path(__file__).parent/'data/patient_demo.csv')
features=['age','bmi','glucose_mg_dl','systolic_bp','cholesterol_mg_dl','smoker']
Xtr,Xte,ytr,yte=train_test_split(df[features],df.risk_group,test_size=.25,random_state=42,stratify=df.risk_group)
model=RandomForestClassifier(n_estimators=250,max_depth=5,random_state=42,class_weight='balanced').fit(Xtr,ytr)
pred=model.predict(Xte)
a,b,c=st.columns(3); a.metric('Demo records',len(df)); b.metric('Test accuracy',f'{accuracy_score(yte,pred):.1%}'); c.metric('Elevated risk records',int((df.risk_group=='Elevated Risk').sum()))
st.dataframe(df,use_container_width=True)
st.subheader('Explore a patient profile')
cols=st.columns(3); age=cols[0].number_input('Age',18,100,45); bmi=cols[1].number_input('BMI',10.0,60.0,26.0); glucose=cols[2].number_input('Glucose mg/dL',40,400,105)
cols=st.columns(3); bp=cols[0].number_input('Systolic BP',60,250,120); chol=cols[1].number_input('Cholesterol mg/dL',80,500,190); smoker=cols[2].selectbox('Smoker',[0,1],format_func=lambda x:'Yes' if x else 'No')
if st.button('Estimate risk',type='primary'):
    out=model.predict(pd.DataFrame([[age,bmi,glucose,bp,chol,smoker]],columns=features))[0]
    st.warning(out)
st.subheader('Evaluation'); st.text(classification_report(yte,pred)); st.dataframe(pd.DataFrame(confusion_matrix(yte,pred)))
st.error('Medical safety: all records are synthetic. Model outputs are not medical advice, diagnosis or treatment recommendations. Consult a qualified clinician for health concerns.')
