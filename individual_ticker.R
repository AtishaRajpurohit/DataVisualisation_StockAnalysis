library(tidyverse)
library(ggplot2)
library(RColorBrewer)
library(plotly)

fundamental=read_csv('5_ratios.csv')
fcol=colnames(fundamental)

#Only select Year 2015
f16=na.omit(fundamental[fundamental$`For Year`==2015,])

#Looking for the distribution of the ratios for dataframe f16
for(col in colnames(f16)){
  print(summary(f16[col]))
}

#Dropping the year column
f16=subset(f16,select=-c(`For Year`))

#Looking at all the ratios
#Ratios for - 
#1. Liquidity Quick Ratio 
#2. Profitability After Tax RoE
#3. Efficiency Asset Utilisation
#4. Market PE Ratio (EPS)
#5. Leverage

#-----------------------Creating a function to select top 10 stocks based on the 5 ratios-----------------------

scale_pivot_df=function(df,col_ratio){
  df[col_ratio]=scale(df[col_ratio],center = FALSE)
  df =df %>% select(col_ratio,'ticker_symbol') %>% 
    pivot_longer(cols = -c('ticker_symbol'),values_to = 'Ratio_Value',names_to = 'Ratio')
  return(df)
}

f17=head(f16 %>% arrange(desc(current_ratio)),10)
f17=scale_pivot_df(f17,'current_ratio')

f18=head(f16 %>% arrange(desc(leverage)),10)
f18=scale_pivot_df(f18,'leverage')

f19=head(f16 %>% arrange(desc(asset_utilisation)),10)
f19=scale_pivot_df(f19,'asset_utilisation')

f20=head(f16 %>% arrange(desc(price_earnings_ratio)),10)
f20=scale_pivot_df(f20,'price_earnings_ratio')

f21=head(f16 %>% arrange(desc(`After Tax ROE`)),10)
f21=scale_pivot_df(f21,'After Tax ROE')

top5=rbind(f17,f18,f19,f20,f21)

top5=top5 %>% mutate(Ratio=case_when(Ratio=='current_ratio'~'Liquidity: Current Ratio',
                                          Ratio=='leverage'~'Gearing: Leverage',
                                          Ratio=='asset_utilisation'~'Efficiency: Asset Utilisation',
                                          Ratio=='price_earnings_ratio'~'Market: Price Earnings',
                                          Ratio=='After Tax ROE'~'Profitibality: After-Tax RoE',))



#colnames(top5)=c('individual','group','value')
data=top5

#------------------------------------------ Circular Barplot --------------------------------------------------

#Generating the id number
data$id <- seq(1, nrow(data))
label_data <- data
number_of_bar <- nrow(label_data)

#Generating angles
angle <- 90 - 360 * (label_data$id-0.5) /number_of_bar# I substract 0.5 because the letter must have the angle of the center of the bars. Not extreme right(1) or extreme left (0)
label_data$hjust <- ifelse( angle < -90, 1, 0)
label_data$angle <- ifelse(angle < -90, angle+180, angle)


empty_bar <- 0
base_data <- data %>% 
  group_by(Ratio) %>% 
  summarize(start=min(id), end=max(id) - empty_bar) %>% 
  rowwise() %>% 
  mutate(title=mean(c(start, end)))

# prepare a data frame for grid (scales)
grid_data <- base_data
grid_data$end <- grid_data$end[ c( nrow(grid_data), 1:nrow(grid_data)-1)] + 1
grid_data$start <- grid_data$start - 1
grid_data <- grid_data[-1,]

# Make the plot
palette_2=c('#2646D1','#7844E1','#E14489','#C91C21','#F46927')
color_plot='#fceee4'
p <- ggplot(data, aes(x=as.factor(id), y=Ratio_Value, fill=Ratio))+
  geom_bar(stat="identity")+
  labs(title = 'Top 10 Tickers for 5 Fundamental Ratios')+#Put margin below
  ylim(-2,3.25) +
  theme(
    #legend.position = "none",
    axis.text = element_blank(),
    axis.title = element_blank(),
    panel.grid = element_blank(),
    axis.ticks = element_blank(),
    panel.background = element_rect(fill = color_plot),
    plot.background = element_rect(fill = color_plot),
    plot.title = element_text(hjust = 0.5),
    plot.subtitle = element_text(hjust = 0.5),
    plot.margin = unit(rep(0,4), "cm"),
    legend.title = element_text(hjust = 0),
    legend.text = element_text(hjust = 0),
  ) +
  scale_fill_manual(values = palette_2)+
  coord_polar() + 
  geom_text(
    data=label_data,
    aes(x=id, y=Ratio_Value+0.35,label=ticker_symbol, hjust=hjust),
    color="black", fontface="bold",
    alpha=0.6, size=2.5,
    angle= label_data$angle,
    inherit.aes = FALSE )
p
#ggsave('top10_circular_barplot.png')

#----------------------------------------------------Scatter Plot 1 PE Ratio versus Leverage----------------------------------------------

#----------------------------------------------------Setting Scatter Plot Theme---------------------------------
theme_sc=theme_minimal()+
  theme(
    axis.title = element_text(hjust = 0.5),
    panel.grid = element_line(linetype = 7),
    panel.grid.minor = element_line(linetype = 3),
    plot.background = element_rect(fill = color_plot),
    #panel.background = element_rect(fill = color_plot),
    plot.title = element_text(hjust = 0.5),
    plot.subtitle = element_text(hjust = 0.5),
    legend.title = element_text(hjust = 0),
    legend.text = element_text(hjust = 0),
  )
  


#Creating the dataset to effectively pick two continous values
f166=f16
f166=f15
ratio_col=c('current_ratio','leverage','asset_utilisation','After Tax ROE','price_earnings_ratio')

for(col in ratio_col){
  f166[[col]]=scale(f166[[col]],center = FALSE)
}

f166=f166 %>% mutate(`Stock Choice`=ifelse((leverage<0.1)&(price_earnings_ratio<0.25),'Preferable Choice','Not Preferable Choice'))
f166=f166 %>% mutate(Stock_Choice_Size=ifelse((leverage<0.1)&(price_earnings_ratio<0.25),0.25,0))

pallete_1=c('#F1A0AD','#D20C2C')
q= ggplot()+
  geom_point(f166,mapping=aes(x=leverage,y=price_earnings_ratio,color=`Stock Choice`,labels=ticker_symbol))+
  #scale_color_brewer(type='seq')+
   labs(title = 'Comparision between Price Earnings Ratio and Leverage',
        
        subtitle = 'Good choice of stocks are colored in red ',
        caption = 'Good choice of stocks, according to these ratios are colored in red ')+
  xlim(0,0.25)+ #Since we require the leverage to be as low as possible
  ylim(0,3)+ #Since we require the PE ratio to be high,however still representative of a healthy company
  xlab('Leverage')+
  ylab('Price Earnings Ratio')+
  theme_sc+scale_color_manual(values=pallete_2)

ggplotly(q)
l <- plotly::ggplotly(q)
htmlwidgets::saveWidget(l, "scatterplot_1.html")

#-----------------------------------Scatter Plot 2 RoE versus Asset Utilisation----------------------------------------------

f166=f166 %>% mutate(`Stock  Choice`=ifelse((asset_utilisation>0.25)&(`After Tax ROE`>0.25),'Preferable Choice','Not Preferable Choice'))
pallete_2=c('#94B4FC','#1633B2')
r= ggplot()+
  geom_point(f166,mapping=aes(x=asset_utilisation,y=`After Tax ROE`,color=`Stock  Choice`,label=ticker_symbol))+
  labs(title = 'Comparision between Asset Utilisation and Return on Equity',
       
       subtitle = 'Good choice of stocks are colored in red ',
       caption = 'Good choice of stocks, according to these ratios are colored in red ')+
  xlim(0,1)+ #Since we require the leverage to be as low as possible
  ylim(0,1)+ #Since we require the PE ratio to be high,however still representative of a healthy company
  xlab('Asset Utilisation')+
  ylab('Return on Equity')+
  theme_sc+scale_color_manual(values=pallete_2)

ggplotly(r)
m <- plotly::ggplotly(r)
htmlwidgets::saveWidget(m, "scatterplot_2.html")











