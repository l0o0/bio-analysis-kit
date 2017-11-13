#!/usr/bin/perl
use strict;
use warnings;
use File::Basename qw(dirname basename);
use FindBin '$Bin';
use lib $Bin;
#use GACP qw(parse_config);

my $path_dir = shift @ARGV;

if (!defined $path_dir){
        print "perl $0 <dir of *.path>\n";
        exit 1;
}

my @list = glob("$path_dir/*.path");
#my $config_file = "$Bin/../config.txt";
#my $Rscript = parse_config($config_file,"Rscript");
foreach my $txt (@list) {
	my $name = $txt;
	my $pdf = $name;
        my $pairwise = basename($name);
        $pairwise =~ s/\.path//;
	$name =~ s/\.path/_cut.txt/g;
	open F, $txt;
	open W, ">$name";
	my $id = 0;
	my $number = 0;
	my $number1 = 0;
	my $number2 = 0;
	my $pvalue = 0;
	my $rich = 0;
	print W "Pathway\tGene_number\tBackgroud_gene_number\tRichFactor\tQvalue\n";
	<F>;
	while (<F>) {
		chomp;
		$id++;
		my @temp = split(/\t/, $_);
		next if (scalar(@temp) < 8);
		$number++;	
		my $path = $temp[0];
		$number1 = $temp[1];
		$number2 = $temp[2];
		$pvalue = $temp[3]; 
		$rich = $number1/$number2;
		$path=~ s/\'//g;
		$path=~ s/\,//g;
		$path=~ s/\-//g;
		print "$number1\t$number2\t$rich\t$pvalue\n";
		print W "$path\t$number1\t$number2\t$rich\t$pvalue\n";	
	}
	close F;
	close W;
	my $plus = $id - $number;
	print "$id\t$number\t$plus\n";
	
open W, ">$pdf.R";
	print W <<QT;
options(bitmapType='cairo')
library(ggplot2);
x <- read.table("$name", head = T, sep = "\\t");
x[,1] = factor(x[,1], levels=rev(x[,1]))
p <- ggplot(x,aes(RichFactor,factor(Pathway)));
p1 = p + geom_jitter(aes(size=Gene_number, colour=Qvalue), position='dodge')+ggtitle("Top 20 Statistics of Pathway Enrichment for $pairwise")+theme(plot.title=element_text(size=14),axis.text= element_text(colour="black",size=9))+theme_bw()+ scale_color_gradientn(colours=rainbow(6))
ggsave("$pdf.enrichment.pdf", width=24, height=18, units='cm')
ggsave("$pdf.enrichment.png", width=10, height=7)
QT
close W;
#system("/nfs2/pipe/RNA/soft/R-3.1.2/bin/Rscript $pdf.R");
system("Rscript $pdf.R");
#system("/nfs/biosoft/ImageMagick-6.9.0-0/local/bin/convert -density 100 $pdf.enrichment.pdf $pdf.enrichment.png");
#system("rm $pdf.R $name");
}

