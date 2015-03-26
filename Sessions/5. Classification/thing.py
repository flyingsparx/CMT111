from wekapy import *

model = Model(classifier_type = "bayes.BayesNet")
model.train(training_file = "contact-lenses.arff")
model.test(test_file = "test.arff")

print model.predictions

for prediction in model.predictions:
        print prediction
