#create a table of the click/open rate per client, per subject, 
# Determine the number of unique subject lines per client

remove(list=ls())
setwd("/Users/Student/Desktop/University/4thYear/4910/input/")

all.data = read.csv("corrected.csv")

num.items.per.client<-data.frame(ClientID=unique(all.data$ClientID), delivered=0, opens=0, clicks=0,avg.opens.per.delivered=0,avg.clicks.per.open=0)

for (client in num.items.per.client$ClientID)
{
  temp.opens.per.client<-sum(all.data$Opened[all.data$ClientID==client])
  temp.delivered.per.client<-sum(all.data$Delivered[all.data$ClientID==client])
  temp.clicks.per.client<-sum(all.data$Clicks[all.data$ClientID==client])
  temp.opens.per.delivered<-sum(all.data$Opened[all.data$ClientID==client], na.rm=T)/sum(all.data$Delivered[all.data$ClientID==client], na.rm=T)
  temp.clicks.per.open<-sum(all.data$Clicks[all.data$ClientID==client], na.rm=T)/sum(all.data$Opened[all.data$ClientID==client], na.rm=T)
  
  num.items.per.client$opens[num.items.per.client$ClientID==client]<-temp.opens.per.client
  num.items.per.client$delivered[num.items.per.client$ClientID==client]<-temp.delivered.per.client
  num.items.per.client$clicks[num.items.per.client$ClientID==client]<-temp.clicks.per.client
  num.items.per.client$avg.opens.per.delivered[num.items.per.client$ClientID==client]<-temp.opens.per.delivered
  num.items.per.client$avg.clicks.per.open[num.items.per.client$ClientID==client]<-temp.clicks.per.open
}

total.avg.opens.per.delivered<-sum(num.items.per.client$opens,na.rm=T)/sum(num.items.per.client$delivered,na.rm=T)
total.avg.clicks.per.open<-sum(num.items.per.client$clicks,na.rm=T)/sum(num.items.per.client$opens,na.rm=T)


num.items.per.subject<-data.frame(SubjectID=unique(all.data$Subject), avg.opens.per.delivered=0,avg.clicks.per.open=0)

for(subject in num.items.per.subject$Subject) {
  temp.opens.per.delivered<-sum(all.data$Opened[all.data$Subject==subject], na.rm = T)/sum(all.data$Delivered[all.data$Subject==subject], na.rm = T)
  temp.clicks.per.open<-sum(all.data$Clicks[all.data$Subject==subject], na.rm = T)/sum(all.data$Opened[all.data$Subject==subject], na.rm = T)
  num.items.per.subject$avg.opens.per.delivered<-temp.opens.per.delivered
  num.items.per.subject$avg.clicks.per.open<-temp.clicks.per.open
}
