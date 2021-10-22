

# ##########################################################################################
# Define a function that brings the indexes of values in a set that are outside the segment
# [ Q1 - 1.5*IQR ; Q3 + 1.5*IQR]
# ##########################################################################################
get_15IQR_outliers_indexes <- function(x, na_rm = TRUE) {
  qnt = quantile(x, probs=c(.25, .75), na.rm = na_rm)
  H = 1.5 * (qnt[2] - qnt[1])
  outliers_indexes = which( x < (qnt[1] - H) | x > (qnt[2] + H))
  return( outliers_indexes)
}

# ##########################################################################################
# Define a function that convert a set of dates named as "ddmmyy" in "yymmdd"
# ##########################################################################################
convert_dates <- function( date_set){
  
  return( sapply( date_set, function( date){
    
    if( nchar( date) == 5){
      date = paste( "0", date, sep="")
    }
    length = nchar( date)
    yy = substr( date, start = length - 1, stop = length)
    mm = substr( date, start = length - 3, stop = length - 2)
    dd = substr( date, start = 1, stop = length - 4)
     
    return (paste (yy, mm, dd, sep=""))
  }))
}

# ##########################################################################################
# Define a function that offers to automatically layout a list of plots in a single viewport
# ##########################################################################################
multiplot <- function( plots=NULL, ncols=1, nrows=0) {
  require(grid)
  
  if( nrows == 0){
    nrows = ceiling( length( plots)/ncols)
  }
  
  numplots = length( plots)
  if( numplots > ncols * nrows){
    stop( "multiplot: To many plots for the numbers of rows and columns:", nrows, "*", ncols)
  }
  
  # Set up the page
  grid.newpage()
  pushViewport(viewport( layout = grid.layout( nrows, ncols)))
  
  # Make each plot, in the correct location
  col=1
  row=1
  for (i in 1:numplots) {
    print(plots[[i]], vp = viewport(layout.pos.row = row,
                                    layout.pos.col = col))
    col = col + 1
    if( col > ncols){
      col = 1
      row = row + 1
    }
  }
}

# ###########################################################################################
# Define a function that produces the min max values on a dataframe for requiested parameters
# ###########################################################################################
get_min_max_x_y <- function( min_max_df, filter_parameter, filter_value, value_parameter_x, value_parameter_y){
  
  result = list()
  result[ "min_x"] = min( min_max_df[ which( min_max_df[ , filter_parameter] == filter_value), value_parameter_x])
  result[ "max_x"] = max( min_max_df[ which( min_max_df[ , filter_parameter] == filter_value), value_parameter_x])
  result[ "min_y"] = min( min_max_df[ which( min_max_df[ , filter_parameter] == filter_value), value_parameter_y])
  result[ "max_y"] = max( min_max_df[ which( min_max_df[ , filter_parameter] == filter_value), value_parameter_y])
  return( result)
}