
# coding: utf-8

# In[1]:

import graphlab as gl

# Load the data
train_data = gl.SFrame('train.csv')
val_data = gl.SFrame('validation.csv')
test_data = gl.SFrame('test.csv')

print(train_data.head(5))
print(val_data.head(5))


# In[3]:

model = gl.boosted_trees_regression.create(train_data, target='click', validation_set=val_data, max_depth =  5, max_iterations=30, features=['weekday', 'hour', 'advertiser'])

# Save predictions to an SFrame (class and corresponding class-probabilities)
predictions = model.predict(val_data)

# Evaluate the model and save the results into a dictionary
results = model.evaluate(val_data)

# Print the new pCTR values
print(predictions.head(5))

# Store the new values into a column called pctr
new_data=val_data.add_column(predictions, name= 'pctr')

# Create new file
new_data.save('predicted_ctr_val.csv', format ='csv')


# In[11]:

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

test_predictions = test_data.add_column(test_predictions, name='pctr')
test_predictions.save('test_predictions.csv', format='csv')


# In[6]:

predicted_data = gl.SFrame('test_predictions.csv')


# In[7]:

predicted_data = predicted_data.sort('pctr', ascending=False)
pctr = predicted_data['pctr']
print pctr.head(10)


# In[23]:

base_bid = 171
actr = train_data['click'].mean()
bid_price = base_bid * pctr / actr
predicted_data.add_column(bid_price, name='bid_price')
predicted_data.print_rows(5,27)


# In[29]:

bids = predicted_data.select_columns(['bidid','bid_price'])
print bids.head(5)


# In[30]:

bids.rename({'bid_price':'bidprice'})
bids.save('testing_bidding_price.csv', format='csv')

