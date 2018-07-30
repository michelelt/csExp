#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 12:12:20 2018

@author: mc
"""
import os
out_str = ""

cities = ["Vancouver", "Berlino", "Milano", "Torino"]
frame_title = ["BookingsPerHour",
               "Distances", 
               "Duration", 
               "Deaths", 
               "AvgStationOccupancy", 
               "AmountRechargePerc", 
               "AvgSOC", 
               "ReroutePerc", 
               "AvgWalkedDistance", 
               "TravelWithPenalty"]
radix_name = ["plot%s/bookginfsPerHour_%s.pdf",
              "plot%s/CDF_%s_distance.pdf",
              "plot%s/CDF_%s_duration.pdf",
              "plot%s/%s_DeathsVsZones_Policy_44_tt-25_100_4.pdf",
              "plot%s/%s_AvgStationOccupancyVsZones_Policy_44_tt-25_100_4.pdf",
              "plot%s/%s_AmountRechargePercVsZones_Policy_44_tt-25_100_4.pdf",
              "plot%s/%s_AvgSOCVsZones_Policy_44_tt-25_100_4.pdf",
              "plot%s/%s_ReroutePercVsZones_Policy_44_tt-25_100_4.pdf",
              "plot%s/%s_AvgWalkedDistanceVsZones_Policy_44_tt-25_100_4.pdf",
              "plot%s/%s_TravelWithPenlatyVsZones_Policy_44_tt-25_100_4.pdf",
              ]
init = '''

\\documentclass{beamer}
\\mode<presentation>
{
	\\usetheme{default}      
	\\usecolortheme{default}
	\\usefonttheme{default}  
	\\setbeamertemplate{navigation symbols}{}
	\\setbeamertemplate{caption}[numbered]
} 

\\usepackage{subfigure}
\\usepackage{lipsum}
\\setbeamertemplate{footline}[frame number]


\\title[Your Short Title]{Comparison Between Cities}
\\author{V1}
\\institute{}
\\date{}

\\begin{document}
	
	\\begin{frame}
	\\titlepage
\\end{frame}

\\begin{frame}{General Metrics}

	\\begin{figure}[ht!]
		\\begin{center}
			
			{
				\\label{fig:agg_bdur}
				\\includegraphics[width=0.45\\textwidth]{../plotAggregated/CDF_aggregate_RentalsDuration.pdf}
			}
			{
				\\label{fig:agg_bdst}
				\\includegraphics[width=0.45\\textwidth]{../plotAggregated/CDF_aggregate_RentalsDistance.pdf}
				
			}
            	{
				\\label{fig:agg_pdst}
				\\includegraphics[width=0.45\\textwidth]{../plotAggregated/CDF_aggregate_ParkingsDuration.pdf}
				
			}
		\\end{center}
		\\label{fig:subfigures}
	\\end{figure}

\end{frame}

\\begin{frame}{Aggregate Bookings per Hour}

	\\begin{figure}[ht!]
		\\begin{center}
			
			{
				\\label{fig:agg_bpd}
				\\includegraphics[width=\\textwidth]{../plotAggregated/aggBookginfsPerHour_Berlino.pdf}
			}
		\\end{center}
		\\label{fig:bpd_}
	\\end{figure}

\end{frame}

\\begin{frame}{HeatMaps}

	\\begin{figure}[ht!]
		\\begin{center}
			
			{
				\\label{fig:hm_V}
				\\includegraphics[width=0.45\\textwidth]{../plotAggregated/Vancouver.png}
			}
			{
				\\label{fig:hm_B}
				\\includegraphics[width=0.45\\textwidth]{../plotAggregated/Berlino.png}
				
			}
			{
				\\label{fig:hm_M}
				\\includegraphics[width=0.45\\textwidth]{../plotAggregated/Milano.png}
			}
			{
				\\label{fig:hm_T}
				\\includegraphics[width=0.35\\textwidth]{../plotAggregated/Torino.jpg}
			}
			
		\\end{center}
		\\label{fig:subfigures}
	\\end{figure}

\\end{frame}


'''

body = '''
\\begin{frame}{%s}

	\\begin{figure}[ht!]
		\\begin{center}
			
			{
				\\label{fig:%s_%s}
				\\includegraphics[width=0.45\\textwidth]{../%s}
			}
			{
				\\label{fig:%s_%s}
				\\includegraphics[width=0.45\\textwidth]{../%s}
				
			}
			{
				\\label{fig:%s_%s}
				\\includegraphics[width=0.45\\textwidth]{../%s}
			}
			{
				\\label{fig:%s_%s}
				\\includegraphics[width=0.45\\textwidth]{../%s}
			}
			
		\\end{center}
		\\label{fig:subfigures}
	\\end{figure}

\\end{frame}
'''


    
        
for i in range(len(radix_name)):
    graphs_list = []
    for city in cities:
        radix_complete = radix_name[i] % (city, city)
        graphs_list.append(radix_complete)
        
    init += body % (frame_title[i], 
                            frame_title[i], city, graphs_list[0], 
                            frame_title[i], city, graphs_list[1], 
                            frame_title[i], city, graphs_list[2], 
                            frame_title[i], city, graphs_list[3] )
    
end = '''
\\end{document}
'''

out = init+end

f = open('/Users/mc/Desktop/csExp/comparisonSlides/slides.tex', 'w')
f.write(out)
f.close()

os.system("pdflatex /Users/mc/Desktop/csExp/comparisonSlides/slides.tex")
os.system("mv slides.aux slides.log slides.nav slides.out lides.pdf slides.pdf slides.snm slides.toc \
           /Users/mc/Desktop/csExp/comparisonSlides/")
