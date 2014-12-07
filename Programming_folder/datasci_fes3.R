log_all<-read.csv(file('/Users/IkkiTanaka/Documents/zozo_analysis/LOG_SEASON.csv',encoding="Shift-JIS"),header=T)
yosoku<-read.csv(file('/Users/IkkiTanaka/Documents/zozo_analysis/ST_01_RECOMMEND/ST_01_RECOMMEND.csv',encoding="Shift-JIS"),header=T)
sortlist<-order(log_all['グループID'])　#グループIDでsort
log_all_sort<-log_all[sortlist,] 
log_1<-log_all_sort[log_all_sort['購入FLG']==1,] #購入したものだけでsort

log_table_all<-table(log_1['商品ID'])

X={}
for (i in 1:length(log_table_all)){#length(log_table_all)
  if (length(subset(yosoku[,1],yosoku['商品ID']==as.numeric(as.character(data.frame(log_table_all)[i,1]))))>0){
    X=rbind(X,data.frame(log_table_all)[i,])
  }
  
}
X=data.frame(X)

labels_all4<-(X[order(X['Freq'],decreasing=T),][1:100,])['Var1']　#購入数が高い商品IDトップ100

kounyu<-{}
etsuran<-{}

kounyu_all<-{}
etsuran_all<-{}

for (i in 1:95){
  #各グループIDのDF抽出
  log_part<-log_all_sort[log_all_sort['グループID']==i,]
  #各グループごとの購入数上位100を用いる
  
  log_1<-log_part[log_part['購入FLG']==1,] #購入したものだけでsort
  log_table<-table(log_1['商品ID'])
  log_table<-data.frame(log_table)
  
  if (nrow(log_table)==0){
    labels<-cbind(data.frame(sample(labels_all4[,1],100,replace=F)),data.frame(rep(0,100)))
    labels<-data.frame(labels)
  }
  
  else{
    labels_all5<-cbind(data.frame(sample(labels_all4[,1],100,replace=F)),data.frame(rep(0,100)))#0は購入数が0
    names(log_table)<-c('商品ID','購入数')
    names(labels_all5)<-c('商品ID','購入数')
    labels_all2<-unique(rbind(labels_all5,log_table))
    labels<-labels_all2[order(-labels_all2[,2]),]
    labels<-data.frame(labels)
  }
  
  if(nrow(labels)<100){
    labels_all5<-cbind(data.frame(labels_all4),data.frame(rep(0,100)))#0は購入数が0
    names(log_table)<-c('商品ID','購入数')
    names(labels_all5)<-c('商品ID','購入数')
    labels_all2<-unique(rbind(log_table,labels_all5)[,1])[1:100]
    labels<-cbind(as.numeric(as.character(labels_all2)),rbind(log_table,labels_all5)[1:100,2])
    labels<-data.frame(labels)
  }
  labels<-labels[1:100,]
  
  names(labels)<-c('商品ID','購入数')
  if (nrow(log_1['グループID'])==0){
    log_1_part<-data.frame(0,0,0,0,0)
    names(log_1_part)<-c('グループID','セッションID','商品ID','購入FLG','閲覧日時')
  }
  else{
    log_1_part<-log_1[log_1['グループID']==i,]
  }
  #購入率
  #セッションIDの総数
  session_all<-nrow(unique(log_part['セッションID']))
  #その商品IDの売れた数
  for (j in 1:100){
    prod_id<-log_part[log_part['商品ID']==as.numeric(as.character(labels[j,1])),]
    session_prod<-nrow(unique(prod_id['セッションID']))
    if ((session_prod>0)&&(is.null(nrow(log_1_part[log_1_part['商品ID']==as.numeric(as.character(labels[j,1])),]))==FALSE)){
      num_prod_id<-nrow(log_1_part[log_1_part['商品ID']==as.numeric(as.character(labels[j,1])),])/session_prod
      
      if (num_prod_id > 0)  {
        kounyu<-append(kounyu,num_prod_id)
        
      }
      else if (num_prod_id == 0){
        kounyu<-append(kounyu,0.01)
      }
      else{
        kounyu<-append(kounyu,0.01)
      }
      
      etsuran_prod<-session_prod/session_all
      etsuran<-append(etsuran,etsuran_prod)
    }
    else{
      kounyu<-append(kounyu,0.001)
      etsuran<-append(etsuran,1.0e-05)
    }
  }
  
  kounyu<-data.frame(kounyu)
  etsuran<-data.frame(etsuran)
  rownames(kounyu)<-NULL
  kounyu_part<-data.frame(append(data.frame(labels[,1]),etsuran))
  kounyu_part<-data.frame(append(kounyu_part,kounyu))
  kounyu_part<-kounyu_part[order(as.numeric(as.character(kounyu_part[,2])),decreasing=T),]
  
  names(kounyu_part)<-c("productID","閲覧率","購入率")
  kounyu_all<-rbind(kounyu_all,kounyu_part)
  if (i == 1){
    names(kounyu_all)<-c("productID","閲覧率","購入率")
  }
  kounyu<-{}
  etsuran<-{}
}


for (i in 1:nrow(kounyu_all)){
  if (kounyu_all[i,3]>0.5){
    kounyu_all[i,3] <- 0.005
  }
  else if(kounyu_all[i,3]==0.5){
    kounyu_all[i,3] <- 0.01
  }
}
kounyu_all$購入率<-(kounyu_all$購入率)/100
kounyu_all<-kounyu_all[,2:3]
#出力
write.csv(kounyu_all,"kounyu.csv",row.names=F)

