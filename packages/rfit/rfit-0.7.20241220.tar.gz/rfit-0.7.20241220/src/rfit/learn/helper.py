# __all__ = ('dfchk')
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.model_selection import PredefinedSplit
# from sklearn.model_selection import GridSearchCV
# from sklearn.model_selection import StratifiedKFold
# from sklearn.metrics import precision_recall_fscore_support
# from sklearn.metrics import roc_auc_score
import requests
import smtplib
from email.mime.text import MIMEText
# from twilio.rest import Client 

#%%
# Standard quick checks
def dfchk(dframe, chkNull=True, info=True, head=True, shape=True, desc=False, valCnt = False): 
  """
  some basic and common checks on dataframes. 
  Args:
      dframe (Pandas.DataFrame): pandas dataframe
      chkNull (bool): check Null option, defaults to True
      info (bool): info option, defaults to True
      head (bool): head option, defaults to True
      shape (bool): shape option, defaults to True
      desc (bool): describe option, defaults to False
      valCnt (bool): value_count option, defaults to False
  Return: None
  """
  cnt = 1
  print('\ndataframe Basic Check function -')
  
  if (chkNull):
    print(f'\n{cnt}: Null values:')
    cnt+=1
    print( dframe.isnull().sum().sort_values(ascending=False) )
  
  if (info):
    try:
      print(f'\n{cnt}: info(): ')
      cnt+=1
      print(dframe.info())
    except: pass
    
  if (desc):
    print(f'\n{cnt}: describe(): ')
    cnt+=1
    print(dframe.describe())
  
  if (head):
    print(f'\n{cnt}: head() -- ')
    cnt+=1
    print(dframe.head())

  if (shape): 
    print(f'\n{cnt}: shape: ')
    cnt+=1
    print(dframe.shape)

  if (valCnt):
    print('\nValue Counts for each feature -')
    for colname in dframe.columns :
      print(f'\n{cnt}: {colname} value_counts(): ')
      print(dframe[colname].value_counts())
      cnt +=1

# examples:
# dfchk(df, desc=True)

#%%
def notify_completion(message, mode={"channel":"slack", "webhook":""}):
    """
    Send message when task is completed
    Args:
        message (str): Content of message
        mode (dict, optional):  {"channel":"slack", "webhook":"" } or  
                                {"channel":"email", "from":"sender@youremail.com", "to": "to_email@youremail.com", "pwd":"", "subject":"Task Completion", "smtp":"smtp.gmail.com", "port":465} or 
                                {"channel":"sms", "twilio_sid":"", "auth_token":"", "from" : "+1234567890", "to": "+0987654321" }. Defaults to "slack" channel.
    """
    channel = mode.get("channel", "slack") # default to slack
    channel = channel.strip().lower()
    if channel=="email":
        try:
            sender_email = mode.get("from", "sender_email@gmail.com")
            to_email = mode.get("to", "to_email@gmail.com")
            body = message
            subject = mode.get("subject", "Task Completion")
            password = mode.get("pwd", "your_password") # App-specific password if using Gmail
            smtp = mode.get("smtp", "smtp.gmail.com")
            port = mode.get("port", 465)
            # Compose the email
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = to_email
            # Send the email
            with smtplib.SMTP_SSL(smtp, port) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, to_email, msg.as_string())
            print("Notification Email sent attempted.")
        except: 
            print("Unknow error, mail did NOT send successfully!")
    elif channel=="sms":
        # Twilio credentials
        account_sid = mode.get("twilio_sid", "your_twilio_account_sid")
        auth_token = mode.get("auth_token", "your_twilio_auth_token")
        from_number = mode.get("from", "+1234567890")  # Your Twilio phone number
        to_number = mode.get("to", "+0987654321") # target phone number
        # Send SMS
        # client = Client(account_sid, auth_token)
        # message = client.messages.create(body=body, from_=from_number, to=to_number )
        # print(f"SMS sent! SID: {message.sid}")
        print("SMS not yet implemented. Notification NOT SENT.")
        
    elif channel=="slack":
        webhook_url = mode.get("webhook", "webhook_url")
        payload = {"text": message}
        requests.post(webhook_url, json=payload)
        print("Slack notification sent!")
    else: # 
        pass

# Send Slack notification
# notify_completion(message="Your model training code completed successfully!", mode={"channel":"slack", "webhook": "https://hooks.slack.com/services/????/???/???" })  


#%%
# from https://github.com/yuxiaohuang/teaching
def common_var_checker(df_train, df_val, df_test, target):
  """
  The common variables checker (Yuxiao Huang)

  Parameters
  ----------
  df_train : the dataframe of training data
  df_val : the dataframe of validation data
  df_test : the dataframe of test data
  target : the name of the target

  Returns
  ----------
  The dataframe of common variables between the training, validation and test data
  """
  
  # Get the dataframe of common variables between the training, validation and test data
  df_common_var = pd.DataFrame(np.intersect1d(np.intersect1d(df_train.columns, df_val.columns), np.union1d(df_test.columns, [target])), columns=['common var'])
              
  return df_common_var
  
#%%
# from https://github.com/yuxiaohuang/teaching
def id_checker(df, dtype='float'):
  """
  The identifier checker (Yuxiao Huang)

  Parameters
  ----------
  df : dataframe
  dtype : the data type identifiers cannot have, 'float' by default
          i.e., if a feature has this data type, it cannot be an identifier
  
  Returns
  ----------
  The dataframe of identifiers
  """
  
  # Get the dataframe of identifiers
  df_id = df[[var for var in df.columns
              # If the data type is not dtype
              if (df[var].dtype != dtype
                  # If the value is unique for each sample
                  and df[var].nunique(dropna=True) == df[var].notnull().sum())]]
  
  return df_id

#%%
# from https://github.com/yuxiaohuang/teaching
def datetime_transformer(df, datetime_vars):
  """
  The datetime transformer (Yuxiao Huang)

  Parameters
  ----------
  df : the dataframe
  datetime_vars : the datetime variables
  
  Returns
  ----------
  The dataframe where datetime_vars are transformed into the following 6 datetime types:
  year, month, day, hour, minute and second
  """
  
  # The dictionary with key as datetime type and value as datetime type operator
  dict_ = {'year'   : lambda x : x.dt.year,
            'month'  : lambda x : x.dt.month,
            'day'    : lambda x : x.dt.day,
            'hour'   : lambda x : x.dt.hour,
            'minute' : lambda x : x.dt.minute,
            'second' : lambda x : x.dt.second}
  
  # Make a copy of df
  df_datetime = df.copy(deep=True)
  
  # For each variable in datetime_vars
  for var in datetime_vars:
      # Cast the variable to datetime
      df_datetime[var] = pd.to_datetime(df_datetime[var])
      
      # For each item (datetime_type and datetime_type_operator) in dict_
      for datetime_type, datetime_type_operator in dict_.items():
          # Add a new variable to df_datetime where:
          # the variable's name is var + '_' + datetime_type
          # the variable's values are the ones obtained by datetime_type_operator
          df_datetime[var + '_' + datetime_type] = datetime_type_operator(df_datetime[var])
          
  # Remove datetime_vars from df_datetime
  df_datetime = df_datetime.drop(columns=datetime_vars)
              
  return df_datetime

#%%
# from https://github.com/yuxiaohuang/teaching
def nan_checker(df):
  """
  The NaN checker (Yuxiao Huang)

  Parameters
  ----------
  df : the dataframe
  
  Returns
  ----------
  The dataframe of variables with NaN, their proportion of NaN and data type
  """
  
  # Get the dataframe of variables with NaN, their proportion of NaN and data type
  df_nan = pd.DataFrame([[var, df[var].isna().sum() / df.shape[0], df[var].dtype]
                          for var in df.columns if df[var].isna().sum() > 0],
                        columns=['var', 'proportion', 'dtype'])
  
  # Sort df_nan in accending order of the proportion of NaN
  df_nan = df_nan.sort_values(by='proportion', ascending=False).reset_index(drop=True)
  
  return df_nan

#%%
# from https://github.com/yuxiaohuang/teaching
def cat_var_checker(df, dtype='object'):
  """
  The categorical variable checker (Yuxiao Huang)

  Parameters
  ----------
  df : the dataframe
  dtype : the data type categorical variables should have, 'object' by default
          i.e., if a variable has this data type, it should be a categorical variable
  
  Returns
  ----------
  The dataframe of categorical variables and their number of unique value
  """
  
  # Get the dataframe of categorical variables and their number of unique value
  df_cat = pd.DataFrame([[var, df[var].nunique(dropna=False)]
                          # If the data type is dtype
                          for var in df.columns if df[var].dtype == dtype],
                        columns=['var', 'nunique'])
  
  # Sort df_cat in accending order of the number of unique value
  df_cat = df_cat.sort_values(by='nunique', ascending=False).reset_index(drop=True)
  
  return df_cat

#%%
# from https://github.com/yuxiaohuang/teaching
def plot_scatter_x1_x2(X, y, xlim, xticks, xlabel, ylim, yticks, ylabel, title, dir_name, fig_name):
  """
  Plot the scatter plot between two features (Yuxiao Huang)
  
  Parameters
  ----------
  X : the feature matrix with two columns
  y : the target vector with two classes, 0 and 1
  xlim : x limits 
  xticks : x ticks
  xlabel : x label
  ylim : y limits 
  yticks : y ticks
  ylabel : y label
  title : the title of the scatter plot
  dir_name : the name of the directory
  fig_name : the name of the figure
  """
  
  # Make directory
  directory = os.path.dirname(dir_name)
  if not os.path.exists(directory):
      os.makedirs(directory)

  # The scatter plot
  plt.scatter(X[y == 1, 0],
              X[y == 1, 1],
              s=100,
              c='b',
              marker='x',
              label='1')
  plt.scatter(X[y == 0, 0],
              X[y == 0, 1],
              s=100,
              c='r',
              marker='s',
              label='0')

  # Set the x-axis
  plt.xlim(xlim)
  plt.xticks(xticks)
  plt.xlabel(xlabel)

  # Set the y-axis
  plt.ylim(ylim)
  plt.yticks(yticks)
  plt.ylabel(ylabel)

  # Set the title and legend
  plt.title(title)
  plt.legend(loc='best')
  
  # Save and show the figure
  plt.tight_layout()
  plt.savefig(dir_name + fig_name)
  plt.show()

#%%
# from https://github.com/yuxiaohuang/teaching
def plot_scatter_tsne(X, y, classes, labels, colors, markers, loc, dir_name, fig_name, random_seed):
  """
  Plot the scatter plot using TSNE (Yuxiao Huang)
  
  Parameters
  ----------
  X : the feature matrix
  y : the target vector
  classes : the classes in the target vector
  labels : the labels for different classes
  colors : the colors for different classes
  markers : the markers for different classes
  loc : the location of the legend
  dir_name : the name of the directory
  fig_name : the name of the figure
  random_seed : the random seed
  """
  
  # Make directory
  directory = os.path.dirname(dir_name)
  if not os.path.exists(directory):
      os.makedirs(directory)

  # Get the tsne transformed training feature matrix
  X_embedded = TSNE(n_components=2, random_state=random_seed).fit_transform(X)

  # Get the tsne dataframe
  tsne_df = pd.DataFrame(np.column_stack((X_embedded, y)), columns=['x1', 'x2', 'y'])

  # Get the data
  data = {}
  for class_ in classes:
      data_x1 = [tsne_df['x1'][i] for i in range(len(tsne_df['y'])) if tsne_df['y'][i] == class_]
      data_x2 = [tsne_df['x2'][i] for i in range(len(tsne_df['y'])) if tsne_df['y'][i] == class_]
      data[class_] = [data_x1, data_x2]
  
  # The scatter plot
  fig = plt.figure(figsize=(8, 6))
  
  for class_, label, color, marker in zip(classes, labels, colors, markers):
      data_x1, data_x2 = data[class_]
      plt.scatter(data_x1, data_x2, c=color, marker=marker, s=120, label=label)

  # Set x-axis
  plt.xlabel('x1')

  # Set y-axis
  plt.ylabel('x2')

  # Set legend
  plt.legend(loc=loc)

  # Save and show the figure
  plt.tight_layout()
  plt.savefig(dir_name + fig_name)
  plt.show()
    
#%%
# from https://github.com/yuxiaohuang/teaching
def separate_duplicate_original(X_aug_train, y_aug_train, minor_class):
  """
  Separate the duplicated class from the original class (Yuxiao Huang)

  Parameters
  ----------
  X_aug_train : The augmented feature matrix
  y_aug_train : The augmented target vector
  minor_class : The minority class
  
  Returns
  ----------
  The separated duplicated class and original class
  """

  # Make a copy of y_aug_train
  y_aug_dup_ori_train = np.array(y_aug_train)
  
  # For each sample in the augmented data
  for i in range(X_aug_train.shape[0]):
      # If the sample has the minor class
      if y_aug_dup_ori_train[i] == minor_class:
          # Flag variable, indicating whether a sample in the augmented data is the same as a sample in the original data
          same = False
          
          # For each sample in the original data
          for j in range(X_aug_train.shape[0]):
              if j == i:
                  continue

              # If the sample has the minor class
              if y_aug_dup_ori_train[j] == minor_class:
                  if len(np.setdiff1d(X_aug_train[i, :], X_aug_train[j, :])) == 0:
                      # The two samples are the same
                      same = True
                      break

          # If the two samples are different
          if same is False:
              y_aug_dup_ori_train[i] = 2
              
  return y_aug_dup_ori_train
  
#%%
# from https://github.com/yuxiaohuang/teaching
def separate_generate_original(X_aug_train, y_aug_train, X_train, y_train, minor_class):
  """
  Separate the generated class from the original class (Yuxiao Huang)

  Parameters
  ----------
  X_aug_train : The augmented feature matrix
  y_aug_train : The augmented target vector
  X_train : The original feature matrix
  y_train : The original target vector
  minor_class : The minority class
  
  Returns
  ----------
  The separated generated class and original class
  """
  
  # Make a copy of y_aug_train
  y_aug_gen_ori_train = np.array(y_aug_train)

  # For each sample in the augmented data
  for i in range(X_aug_train.shape[0]):
      # If the sample has the minor class
      if y_aug_gen_ori_train[i] == minor_class:
          # Flag variable, indicating whether a sample in the augmented data is the same as a sample in the original data
          same = False

          # For each sample in the original data
          for j in range(X_train.shape[0]):
              # If the sample has the minor class
              if y_train[j] == minor_class:
                  if len(np.setdiff1d(X_aug_train[i, :], X_train[j, :])) == 0:
                      # The two samples are the same
                      same = True
                      break

          # If the two samples are different
          if same is False:
              y_aug_gen_ori_train[i] = 2
              
  return y_aug_gen_ori_train

#%%
# from https://github.com/yuxiaohuang/teaching
def get_train_val_ps(X_train, y_train, X_val, y_val):
  """
  Get the:
  feature matrix and target velctor in the combined training and validation data
  target vector in the combined training and validation data
  PredefinedSplit
  
  Parameters
  ----------
  X_train : the feature matrix in the training data
  y_train : the target vector in the training data
  X_val : the feature matrix in the validation data
  y_val : the target vector in the validation data  

  Return
  ----------
  The feature matrix in the combined training and validation data
  The target vector in the combined training and validation data
  PredefinedSplit
  """  

  # Combine the feature matrix in the training and validation data
  X_train_val = np.vstack((X_train, X_val))

  # Combine the target vector in the training and validation data
  y_train_val = np.vstack((y_train.reshape(-1, 1), y_val.reshape(-1, 1))).reshape(-1)

  # Get the indices of training and validation data
  train_val_idxs = np.append(np.full(X_train.shape[0], -1), np.full(X_val.shape[0], 0))

  # The PredefinedSplit
  ps = PredefinedSplit(train_val_idxs)

  return X_train_val, y_train_val, ps

#%%
# NOT working
# from https://github.com/yuxiaohuang/teaching
# def training_valation_test(X_train, y_train, X_test, y_test, ps, abspath_curr, name):
#   """
#   Training, validation and test (Yuxiao Huang)
  
#   Parameters
#   ----------
#   X_train : the feature matrix in the training data
#   y_train : the target vector in the training data
#   X_test : the feature matrix in the test data
#   y_test : the target vector in the test data    
#   ps : the PredefinedSplit
#   abspath_curr : the absolute path of the current folder
#   name : the name of the cv_results folder

#   Return
#   ----------
#   The dataframe of [precision, recall, best_estimator]
#   """    
  
#   #************************************************************************************************
#   # Creating the directory for the cv results
#   directory = os.path.dirname(abspath_curr + name + '/')
#   if not os.path.exists(directory):
#       os.makedirs(directory)
      
#   #************************************************************************************************
#   # Training and validation

#   # The list of [best_score_, best_params_, best_estimator_] obtained by GridSearchCV
#   best_score_param_estimator_gs = []

#   for acronym in pipes.keys():
#       # GridSearchCV
#       gs = GridSearchCV(estimator=pipes[acronym],
#                         param_grid=param_grids[acronym],
#                         scoring='f1',
#                         n_jobs=2,
#                         cv=ps,
#                         return_train_score=True)

#       # Fit the pipeline
#       gs = gs.fit(X_train, y_train)

#       # Update best_score_param_estimator_gs
#       best_score_param_estimator_gs.append([gs.best_score_, gs.best_params_, gs.best_estimator_])

#       # Sort cv_results in ascending order of 'rank_test_score' and 'std_test_score'
#       cv_results = pd.DataFrame.from_dict(gs.cv_results_).sort_values(by=['rank_test_score', 'std_test_score'])

#       # Get the important columns in cv_results
#       important_columns = ['rank_test_score',
#                             'mean_test_score', 
#                             'std_test_score', 
#                             'mean_train_score', 
#                             'std_train_score',
#                             'mean_fit_time', 
#                             'std_fit_time',                        
#                             'mean_score_time', 
#                             'std_score_time']

#       # Move the important columns ahead
#       cv_results = cv_results[important_columns + sorted(list(set(cv_results.columns) - set(important_columns)))]

#       # Write cv_results file
#       cv_results.to_csv(path_or_buf=abspath_curr + name + '/' + acronym + '.csv', index=False)

#   #************************************************************************************************
#   # Test

#   # The list of [precision, recall, fscore, auc, best_estimator]
#   precision_recall_fscore_auc_best_estimator = []

#   for best_score, best_param, best_estimator in best_score_param_estimator_gs:
#       # Get the prediction
#       y_pred = best_estimator.predict(X_test)

#       # Get the precision, recall, fscore, support
#       precision, recall, fscore, support = precision_recall_fscore_support(y_test, y_pred)

#       # Get the auc
#       auc = roc_auc_score(y_test, y_pred)

#       # Update precision_recall_fscore_auc_best_estimator
#       precision_recall_fscore_auc_best_estimator.append([precision, recall, fscore, auc, best_estimator])

#   # Return precision_recall_fscore_best_estimator
#   return pd.DataFrame(precision_recall_fscore_auc_best_estimator, columns=['Precision', 'Recall', 'F1-score', 'AUC', 'Model'])


#%%