args<-commandArgs(T)

library(ggplot2)
library(grid)
colours=c("#29B5F0", "#EB5A28" ,"#36D750","#ffffb3")
d=read.table(args[1],sep="\t",stringsAsFactors=F)
file=strsplit(args[1],"/")[[1]][length(strsplit(args[1],"/")[[1]])]
sample=strsplit(file,"\\.")[[1]][1]
values=d$V2
d$V1=factor(d$V1,levels=d$V1,order=TRUE)
percent_str <- paste(round(values/sum(values) * 100,4), "%", sep="")
values <- data.frame(Percentage = round(values/sum(values) * 100,4), Part = d$V1,percent=percent_str )
lab_legend=paste(paste((paste(d$V1,d$V2,sep=" (")),values$percent,sep=","),")",sep="")
out=paste(sample,".readsClass.png",sep="")
ggtitle1=paste(paste("Partition of Raw Reads(",sample,sep=""),")",sep="")
png(out,width=600,height=600)
ggplot(values, aes(x="",y=Percentage,fill=Part)) +  geom_bar(stat="identity",width=3,color="#555555") +coord_polar("y")+xlab('')+ylab('')+labs(fill="")+scale_fill_manual(values=colours,labels=lab_legend)+theme(axis.ticks=element_blank(),axis.text=element_blank(),panel.grid=element_blank())+ggtitle(ggtitle1)+theme(legend.text = element_text(size = 12, family = "Arial"), plot.title=element_text(size=18, family = "Arial",face="bold"), plot.margin=unit(c(0.1,1.2,0.1,0.4),"cm"))+guides(fill=guide_legend(keywidth=1,keyheight=1.2))
dev.off()

