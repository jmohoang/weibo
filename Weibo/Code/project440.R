#
#Libraries 
#
library(gbm)
library (lubridate)

#
#Preparations
#
overall = read.csv("overall.csv")
overall$hour <- as.factor(hour(hms(overall$OriginalTime)))
overall$OriginalTime <- NULL
#We got read of the time valuesand kept only the hour of the day.

set.seed(1)
train = sample(nrow(overall), 2/3 * nrow(overall))
test = -train

#
#Logistic regression
#
glm.fit = glm(Retweeted ~ ., data = overall[train, ], family = binomial)
summary(glm.fit)
glm.probs = predict(glm.fit, newdata = overall[test, ], type = "response")
glm.pred = rep(0, length(glm.probs))
glm.pred[glm.probs > 0.5] = 1
# Confusion Matrix based on Logistic regression
table(glm.pred, overall$Retweeted[test])

mean(glm.pred != overall$Retweeted[test])
#Validation test Error rate = 0.2259

#
#Tree Model 
#
tree.overall = tree(Retweeted ~., subset = train, data = overall[train,])
summary(tree.overall)
#From this we see that UserActivenss and Textlength play a large role. 
plot(tree.overall)
text(tree.overall)

tree.probs = predict(tree.overall, newdata = overall[test, ])
tree.pred = rep(0, length(tree.probs))
tree.pred[tree.probs > 0.5] = 1
# Confusion Matrix based on Logistic regression
table(tree.pred, overall$Retweeted[test])

mean(tree.pred != overall$Retweeted[test])
#Validation test Error rate = 0.22693


##
## Boosted Tree Model 
##
#boost.overall = gbm(Retweeted ~ ., 
#                   data = overall, 
#                   distribution = "bernoulli", 
#                   n.trees = 500)
#summary(boost.overall)
#yhat.boost = predict(boost.overall, newdata = overall[test, ], n.trees = 500)
#yhat.pred = rep(0, length(yhat.boost))
#yhat.pred[yhat.boost > 0.5] = 1
#table(yhat.pred, overall$Retweeted[test])

#mean(yhat.pred != overall$Retweeted[test])
##Validation Tets error rate is 0.50266
