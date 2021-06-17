import pandas as pd

from PrepareDataset.prepareDataset import scrape

if __name__ == '__main__':
	scrapeObj = scrape()
	driver = scrapeObj.getDriver()

	scrapeObj.loginToFacebook(driver)

	queryList = ['oxygen%20required', 'bed%20required', 'hospital%20bed%20required', 'blood%20required', 'oxygen%20need', 'blood%20need', 'oxygen', 'bed', 'hospital', 'blood']
	dflist = []
	for query in queryList:
		df = scrapeObj.getDataSet(query, driver)
		dflist.append(df)

	driver.close()

	outputDataSet = pd.concat(dflist, ignore_index=True)
	outputDataSet.to_csv('PrepareDataset\dataset.csv')
	print("Dataset Preparation Complete")