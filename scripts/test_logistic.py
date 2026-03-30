from stock_prediction.models.logistic_model import LogisticModel

def main():

    model = LogisticModel()
    model.train()

if __name__=="__main__":
    main()