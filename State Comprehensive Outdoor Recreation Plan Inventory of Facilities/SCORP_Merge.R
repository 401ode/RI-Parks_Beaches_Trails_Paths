# Author: RKelly 
# Date: 5/23/2016
# Goal: Match GoRI Summaries back to Master SCORP File
  # Open Datasets
  # Check for Duplicate ID's
  # Merge on ID
  # Save file



merged.scorp <- merge(MasterSCORP_GoRI, Conservation.Area.Survey, by="ID", all.x=TRUE)

write.table(merged.scorp,"C:\\Users\\Ryan.Kelly\\Documents\\GitHub\\RI-Recreational Areas\\State Comprehensive Outdoor Recreation Plan Inventory of Facilities\\Merged_SCORP.txt", sep="\t")