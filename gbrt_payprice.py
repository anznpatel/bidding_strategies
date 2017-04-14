
# coding: utf-8

# In[1]:

import graphlab as gl

# Load the data
train_data = gl.SFrame('train.csv')
val_data = gl.SFrame('validation.csv')
test_data = gl.SFrame('test.csv')

print(train_data.head(5))
print(val_data.head(5))


# In[2]:

model = gl.boosted_trees_regression.create(train_data, target='payprice', validation_set=val_data, max_depth =  5, max_iterations=30, features=['slotprice', 'useragent', 'advertiser','adexchange', 'slotvisibility'])

# Save predictions to an SFrame (class and corresponding class-probabilities)
predictions = model.predict(val_data)

# Evaluate the model and save the results into a dictionary
results = model.evaluate(val_data)

# Print the new predicted pay price values
print(predictions.head(5))

# Store the new values into a column called pctr
new_data=val_data.add_column(predictions, name= 'ppayprice')

# Create new file
new_data.save('predicted_payprice_val.csv', format ='csv')


# In[4]:

# Save predictions to an SFrame (class and corresponding class-probabilities)
test_predictions = model.predict(test_data)

# Evaluate the model and save the results into a dictionary
#test_results = model.evaluate(test_data)

# Check how each feature has an impact on the predictions, positive or negative
#test_coefs = model['coefficients']
#print test_coefs

# Print the new pCTR values
print(test_predictions.head(5))


# In[5]:

test_predictions = test_data.add_column(test_predictions, name='payprice')
test_predictions.save('test_predictions_payprice.csv', format='csv')


# In[7]:

predicted_data = gl.SFrame('test_predictions_payprice.csv')


# Mixing the two models (bidprice by pCTR and pCPC)

# In[8]:

predicted_data = predicted_data.sort('payprice', ascending=True)
pay_price = predicted_data['payprice']
print pay_price.head(10)

