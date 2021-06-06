import pandas as pd

from PrepareDataset.prepareDataset import scrape

if __name__ == '__main__':
	scrapeObj = scrape()
	driver = scrapeObj.loginToFacebook()

	queryList = ['oxygen', 'bed']

	dflist = []
	for query in queryList:
		df = scrapeObj.getDataSet(query, driver)
		dflist.append(df)

	driver.close()

	outputDataSet = pd.concat(dflist, ignore_index=True)
	outputDataSet.to_csv('PrepareDataset\dataset.csv')
	print("Dataset Preparation Complete")