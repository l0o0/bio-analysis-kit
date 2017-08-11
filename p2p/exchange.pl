#!/usr/bin/perl
#This program is to change the name and filter repeat
#created by liyan 2016.08.20  liyan1606@1gene.com.cn

use strict;
use Getopt::Long;
use FindBin qw($Bin $Script);
use File::Basename;
use lib $Bin;
my ($filter,$protein,$outdir,$final,$help);
GetOptions(
        "filter:s"=>\$filter,
        "protein:s"=>\$protein,
	"out:s"=>\$outdir,
	"final:s"=>\$final,
        "help!"=>\$help
);

sub usage{
    print <<EOF;
Usage:
    perl $0 -filter filter.txt -protein 4577.protein.links.v10.txt.gz -out out.gz -final final.txt.gz
EOF
}
#print "$protein\n";
&usage() if($help);
&usage() unless ($filter and $outdir and $protein);
my %hash;
open(FILTER,"$filter") || die "$!";
while(<FILTER>){
    chomp;
    my @array = split /\t/,$_;
    my $key = $array[0];
    my $value = $array[1];
    $hash{$key} = $value;
}
close(FILTER);
open(OUT,">$outdir") || die "$!";
open OUT, "| gzip >$outdir" or die $!;
print OUT "#proteion1\tproteion2\tscore\n";
open(IN,"gzip -dc $protein |") || die "$!";
while(<IN>){
    chomp;
    next if ($_ =~ /protein1/);
    my ($protein1,$protein2,$score) = split /\s+/,$_;    
    if(defined $hash{$protein1} && defined $hash{$protein2}){
	print OUT "$hash{$protein1}\t$hash{$protein2}\t$score\n";
    }
}
close(OUT);
close(IN);

my %final;
open(IN,"gzip -dc $outdir |") || die "$!";
open(OUT,"| gzip >$final") || die "$!";
print OUT "#proteion1\tproteion2\tscore\n";
while(<IN>){
    chmod;
    next if ($_ =~ /^#/);
    my @tmp = split /\t/,$_;
    my $sample1 = ($tmp[0] lt $tmp[1]) ? $tmp[0] : $tmp[1];
    my $sample2 = ($tmp[0] lt $tmp[1]) ? $tmp[1] : $tmp[0];
    next if (exists $final{$sample1."\t".$sample2});
    $final{$sample1."\t".$sample2} = 1;
    print OUT "$tmp[0]\t$tmp[1]\t$tmp[2]";
}
close(IN);
close(OUT);







