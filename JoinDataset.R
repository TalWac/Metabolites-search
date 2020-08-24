#install.packages("readxl")
library("readxl") # for import excel
library("fuzzyjoin") # to join similar columns  string similarity
library("stringdist") # to join similar columns  string similarity
library("dplyr") # the the %>% operatore
library("miceadds") # to load Rdata files convinientely 
#library("qdapDictionaries")


# The fucntion joind the HMDB list data made by the Short_Parser_HMDB function
# with the Excel file which is the ouput of the LCMS it tries to join bu inchikey if exists on the excel list otherwise
# by formula name (name)

joindata<- function(hmdb.list, excel.file.path){
  
  # import / load data 
  
  
  # excel.file.path is Excel file - the oupt put of MC-LS 
  # hmdb.list is a list Rdata file from the HMDB  its the oupput of Parser_HMDB\ Short_Parser_HMDB function 
  
  #load(file = "hmdb.list") # to object called Short_outp
  load.Rdata(filename = "hmdb.list", "hmdb")
  excel.list <- read_xlsx(path="excel.file.path", col_names = TRUE)
  
  #change to dataframes and give a names to columns
  df.hmdb<-data.frame(matrix(unlist(hmdb), nrow=length(hmdb), byrow=T))
  names(df.hmdb) <- c("accession","name","inchikey")
  
  excel.list<-as.data.frame(excel.list)
  
  
  # join data by common inchikey
  joindata.by.inchikey <- merge(x=df.hmdb,y=excel.list, by.x=c("inchikey"), by.y=c("InChIKey"))
  
  # join data by common formula name when InChIKey value is NA in excel.list data
  joindata.by.name <- merge(x=df.hmdb,y=excel.list[is.na(excel.list$InChIKey), ], by.x=c("name"), by.y=c("Name"))
  
  # join the data fram by similar name after reducing to only what we have not find a match in the prviews joins  
  # df.hmdb without rows that already had match in joindata.by.inchikey
  df.hmdb.reduce<-df.hmdb[ !df.hmdb$inchikey  %in% joindata.by.inchikey$inchikey    , ]
  
  # df.hmdb without rows that already had match in joindata.by.inchikey and row aready match in joindata.by.name
  df.hmdb.reduce1<-df.hmdb.reduce[!df.hmdb.reduce$inchikey  %in% joindata.by.name$inchikey ,]
  
  # excel.list data only with NA values in InChIKey variable and reduced rows that already find a match by name in  data df.hmdb
  excel.list.reduce<- excel.list[is.na(excel.list$InChIKey), ][!excel.list[is.na(excel.list$InChIKey), ]$Name %in% joindata.by.name$name, ]
  
  joindata.reduc <- df.hmdb.reduce1 %>%
    stringdist_inner_join(excel.list.reduce, by = c(name = "Name"), max_dist =1 ,    distance_col="distance_col" )
  
  names(joindata.by.inchikey)
  names(joindata.by.name)
  
  # reorder the colums in the data sets and append using rbind
  joindata.all<-rbind(
    
    joindata.by.inchikey[, c("accession", "inchikey", "name", "Structure", "Formula",
                             "Molecular Weight", "CSID" ,"# References","CID","SMILES")],
    
    joindata.by.name[, c("accession", "inchikey", "name", "Structure", "Formula",
                         "Molecular Weight", "CSID" ,"# References","CID","SMILES")],
    
    joindata.reduc.reduc[, c("accession", "inchikey", "name", "Structure", "Formula",
                             "Molecular Weight", "CSID" ,"# References","CID","SMILES")]
  )
  
  
  
}



# import / load data 

load(file = "D:/BCDD/Documents/Tal/Projects/HMDB/Rdata/Short_saliva_metabolites_List.Rdata")
test_larger_list <- read_xlsx(path="D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/test_larger_list.xlsx", col_names = TRUE)

hmdb
#change to dataframes and give a names to columns
df.saliva<-data.frame(matrix(unlist(Short_outp), nrow=length(Short_outp), byrow=T))
names(df.saliva) <- c("accession","name","inchikey")

test_larger_list<-as.data.frame(test_larger_list)


# join data by common inchikey
joindata.by.inchikey <- merge(x=df.saliva,y=test_larger_list, by.x=c("inchikey"), by.y=c("InChIKey"))

# join data by common formula name when InChIKey value is NA in test_larger_list data
joindata.by.name <- merge(x=df.saliva,y=test_larger_list[is.na(test_larger_list$InChIKey), ], by.x=c("name"), by.y=c("Name"))

# join the data fram by similar name after reducing to only what we have not find a match in the prviews joins  
# df.saliva without rows that already had match in joindata.by.inchikey
df.saliva.reduce<-df.saliva[ !df.saliva$inchikey  %in% joindata.by.inchikey$inchikey    , ]

# df.saliva without rows that already had match in joindata.by.inchikey and row aready match in joindata.by.name
df.saliva.reduce1<-df.saliva.reduce[!df.saliva.reduce$inchikey  %in% joindata.by.name$inchikey ,]

# test_larger_list data only with NA values in InChIKey variable and reduced rows that already find a match by name in  data df.saliva
test_larger_list.reduce<- test_larger_list[is.na(test_larger_list$InChIKey), ][!test_larger_list[is.na(test_larger_list$InChIKey), ]$Name %in% joindata.by.name$name, ]

joindata.reduc <- df.saliva.reduce1 %>%
  stringdist_inner_join(test_larger_list.reduce, by = c(name = "Name"), max_dist =1 ,    distance_col="distance_col" )

names(joindata.by.inchikey)
names(joindata.by.name)

# reorder the colums in the data sets and append using rbind
joindata.all<-rbind(

joindata.by.inchikey[, c("accession", "inchikey", "name", "Structure", "Formula",
                         "Molecular Weight", "CSID" ,"# References","CID","SMILES")],

joindata.by.name[, c("accession", "inchikey", "name", "Structure", "Formula",
                     "Molecular Weight", "CSID" ,"# References","CID","SMILES")],

joindata.reduc.reduc[, c("accession", "inchikey", "name", "Structure", "Formula",
                 "Molecular Weight", "CSID" ,"# References","CID","SMILES")]
)

