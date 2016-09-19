#setup and import libraries

import pandas as pd 

#function to split space delimited dataframe columns
#as generated by multi-selects in an ona form
def split_space_delimited(df,col):

	"""Function to parse space-delimited data in a DataFrame column.

	Will split columns into multiple columns and return a copy of original
	dataframe with new columns added.  Drops rows where col to split is null."""

	#begin by removing null values of the column to split from the dataframe
	df_notnull = df.loc[df[col].notnull()]
	df_notnull = df_notnull.reset_index().drop('index',axis=1)

	#create dataframe of space-delimited values in column
	df_split = pd.DataFrame(df_notnull[col].str.split(' ').tolist())

	#rename columns with meaninful names
	for num in df_split.columns:
		newcol = col + '_' + str(num)
		df_split = df_split.rename(columns={num:newcol})

	df_final = df_notnull.join(df_split)

	return df_final

def trans_space_delimited(df,splitcol,groupcols):

    """Function to split space delimited column, and return a DataFrame containing all 
    items in the column gropued by other dataframe columns of your choice.
    
    usage:
    
    df_new = trans_space_delimited(df_old,splitcol='col',groupcols=['col1','col2'...])
    
    """
    #drop null values of split col from df
    df_notnull = df.loc[df[splitcol].notnull()]
    df_notnull.reset_index().drop('index',axis=1,inplace=True)
    
    #limit dataframe to relevant columns
    allcols = groupcols.copy()
    allcols.append(splitcol)

    df_lim = df_notnull.loc[:,allcols]
    
    #split delimited column, and create new dataframe of split values
    df_split = pd.DataFrame(df_lim[splitcol].str.split(' ').tolist())
    
    #rename split columns
    for col in df_split:
        newcol = splitcol + '_' + str(col)
        df_split = df_split.rename(columns={col:newcol})
    
    #join split columns to original dataframe
    df_merge = df_lim.join(df_split)
    
    #transpose dataframe
    df_trans = pd.melt(df_merge,id_vars=groupcols,value_vars=[x for x in df_merge.columns if x.startswith(splitcol + '_')])

    return df_trans

def unpack_repeat(df,repeatcol,mergecols=None):
    
    """Function to extract data from columns of repeated questions in Ona.  Returns a new dataframe,
    optionally also containing other, non-repeated columns of data from the original DataFrame
    mapped to the unpacked repeated column."""
    
    stacked = None
    
    df = df.loc[df[repeatcol].notnull()]
    
    for i in range(0,len(df)):
        to_unpack = df.iloc[i,df.columns.tolist().index(repeatcol)]
        unpacked_row = pd.DataFrame(to_unpack)
        
        for col in unpacked_row:
            newcol = col.split('/')[-1]
            unpacked_row = unpacked_row.rename(columns={col:newcol})
            
        if mergecols != None:
            for col in mergecols:
                unpacked_row[col] = df.iloc[i,df.columns.tolist().index(col)]
            
            
        if i == 0:
            stacked = unpacked_row.copy()
        else:
            stacked = stacked.append(unpacked_row)
            
    #reorder columns - merged cols at left
    col_order = mergecols + [x for x in stacked.columns if x not in mergecols]
    stacked = stacked[col_order]
    
    stacked = stacked.reset_index().drop('index',axis=1)
    
    return stacked
    
    


	



