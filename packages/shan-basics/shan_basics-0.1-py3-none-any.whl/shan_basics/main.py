def print_python_libraries():
    a = r"""
    Pandas:

  pd.Timestamp.now() ===> current date via pandas
  pd.Categorical(df['label']).codes ===> label encoding via pandas
  from sklearn.preprocessing import LabelEncoder
  df['label'] = LabelEncoder.fit_transform(df['label'])

  Pandas_codes():
    import pandas as pd
    df1 = pd.DataFrame({'marks':[80,90,100], 'rank': [3,2,1]}, index = ['StudentA', 'StudentB', 'StudentC'])
    print(df1)
    df2 = pd.DataFrame({'grade':['C','B','A'], 'rank': [3,2,1]}, index=[1,2,3])
    print(df2)
    df = pd.merge(df1,df2,on='rank')
    print(df)
    df3 = pd.DataFrame({'CGPA':[8,9,10]})
    df_ = pd.concat([df,df3]) # df.append(df3) works the same
    print(df_)
    df_= pd.concat([df,df3], axis=1)
    print(df_)
    print(df_.corr())
    import seaborn as sns
    import matplotlib.pyplot as plt
    map = sns.heatmap(df_.corr(), annot = True, cmap = 'coolwarm', linewidths = 10) #linewidths = space b/w each box, annot is used to show names on boxes
    #plt.show()
    change = {'A':1.0,'B':2.0,'C':3.0}
    df_['grade'] = df_['grade'].map(change)
    print(df_)
    print(df_.dtypes)
    df_ = df_.rename(columns = {'CGPA':'Point'})
    print(df_)
    df4 = pd.DataFrame({'Status':['follower', 'follower', 'leader']})
    df_ = pd.concat([df_,df4], axis = 1)
    print(df_)
    df5 = pd.get_dummies(df_['Status'])
    print(df5)
    df_ = pd.concat([df_,df5], axis = 1)
    print(df_)
    print(df_.shape)
    a = [1,2,3,4]
    _df = pd.Series(['a','b','c'], index = [1,2,3], name = 'Series')
    print(_df)

    fruit = ['Apple', 'Orange', 'Grapes']
    rate = [80, 45, 40]
    health = ['A', 'B', 'C']
    shop = pd.Series(rate, fruit) # right
    # shop = pd.Series(rate, fruit, health) # wrong
    shopee = pd.DataFrame(rate, fruit)
    print(shop)
    print(shopee)
    print(".................")
    df_=pd.read_csv(r"C:\Users\DELL\Desktop\Mini_project2\water_potability.csv")
    print(df_.columns, df_.describe, df_.info)

    import pandas as pd
    import numpy as np
    df = pd.read_csv(r'C:\Users\DELL\Downloads\wine.csv')
    # changing all values of a data frame by a specific formuls
    df['quality_Q'] = df['quality'].apply(lambda x:x*100)
    # or
    df['quality_QQ'] = df['quality'].map(lambda x:x*1000)
    #or
    df['quality_QQQ'] = df['quality'] * 10000
    print(df[['quality', 'quality_Q', 'quality_QQ' ,'quality_QQQ']])
    print(df)
    print(df.quality_QQ.unique())
    df.apply(lambda x: x*100)
    print(df)

    import pandas as pd
    import numpy as np
    df = pd.DataFrame(np.random.rand(5,3), index=[5,3,2,4,1], columns = list('ABC'))
    # for a specific row
    print(df)
    print(df.loc[1]) #for a specific index calling wrt no
    print(df.iloc[1]) # for a specific index calling wrt location {location starts from 0}
    #Sorting
    print(df.sort_index())
    print(df.sort_index(ascending = False))
    #Slicing
    df = df.sort_index()
    print(df.head(3))
    print(df.tail(3))
    print(df[1:4])

    import pandas as pd
    import numpy as np
    df = pd.DataFrame([[10,15,12], [np.NaN, 13, 10], [14, np.NaN, 13], [np.NaN, np.NaN, 14], [13,12,11]], index = [1,2,3,4,5], columns = ['A', 'B', 'C'])
    print(df)
    df1 = df.dropna(subset = ['col name'], axis = 0 , inplace - True) # list wise deletion
    print(df1)
    df2 = df.dropna(subset = ['col name'], axis = 1 , inplace - True) # pair wise deletion
    print(df2)

    df = df['col name']
    df4 = df.fillna(method = 'ffill')
    print(df4)
    df5 = df.fillna(method = 'bfill')
    print(df5)
    df3 = df.fillna(0)
    print(df3)
    df6 = df.fillna(df.mean()) #or df.median / df.mode() / df.max() / df.min()
    print(df6)
    df10 = df.replace(np.nan, df.mean())

    print(df.isnull().sum())
    #df7 = df.fillna(subset = ['B']) ???????????????????????????????????????
    #print(df7) ??

    import pandas as pd
    import numpy as np
    df = pd.read_csv(r'C:\Users\DELL\Downloads\wine.csv')
    print(df.describe(include = 'all')) # include = 'all' implies all the columns must be considered for describing
    print(df.info())
    print(df[['pH', 'type']].groupby(['type'], as_index=False).mean())
    print(df[['pH', 'type']].groupby(['type'], as_index=True).mean())
    print(df[['type', 'quality', 'density']].groupby(['type', 'quality'], as_index = False).mean())
    print(df.groupby(['type'], as_index = False).mean())

    print(df[df['quality']>5][['pH', 'quality', 'density']].groupby(['quality'], as_index=False).mean())
    print(df[df['quality']>5][['pH', 'quality', 'density','type']].groupby(['quality', 'type'], as_index=False).mean())

    print(df[['density', 'pH', 'quality']].groupby(['quality'], as_index=True).agg([np.sum, np.mean, np.std]))

    print(df.groupby('quality').filter(lambda x: len(x)>=50)) # ??????????????????

  link: https://towardsdatascience.com/an-introduction-to-pandas-in-python-b06d2dd51aba
  link_from_PPB: https://colab.research.google.com/drive/13iWNFfaJAU0BtPhIDvHHZUzGXO7YLlUC?usp=sharing
  for data manipulation
  types of data structures in pandas: DataFrame{for 2D arrays} + Series{ for 1D arrays}

  PLOTTING
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    df = pd.DataFrame(np.random.rand(10,4), columns = list('ABCD'))
    print(df)

    plt.figure(figsize =(20,20))
    sns.heatmap(df.corr(), annot = True, cmap = 'coolwarm', linewidths = 2)

    df.plot.scatter(x = 'A', y  = 'B')
    for each trial:
    df.plot()
    df.plot.bar()
    df.plot.bar(stacked = True) ??
    df.plot.barh()
    for each column:
    df.hist(bins=10) - - gives column wise frequency
    df.plot.hist(bins = 10)
    df.plot.area() ??
    df.plot.box() - column wise values mean,...
    df.plot.pie(subplots = True)

  MAKING A DATAFRAME
    2D
    df = pd.DataFrame({'marks':[25,35], 'rank':[1,2]}, index = ["StudentA", "StudentB"], name='dataframe name')
    or
    df = pd.DataFrame({[25,35], [1,2]}, index =  ["StudentA", "StudentB"], column = ['marks', 'rank'])
    #when index is not mentioned 0,1,2... are taken as default
    # similar to dictionaries
    1D
    df = pd.Series([1,2,3], index = ['a','b','c'], name = 'Series name')
    1D + 2D
    fruit = ['Apple', 'Orange', 'Grapes']
    rate = [80, 45, 40]
    health = ['A', 'B', 'C']
    shop = pd.Series(rate, fruit) # right
    shopee = pd.DataFrame(rate, fruit) # right
    # shop = pd.Series/DataFrame(rate, fruit, health) # wrong

  MERGING DATAFRAME
    pd.merge(df1, df2, on='common_column name', how='left/right/inner/outer')
    # consider sets df1 and df2
    inner = common of both
    left = common of both + left xtra
    right = common of both + right xtra
    outer = all

  OPENING A DATAFRAME
    pd.read_csv / pd.read_excel / pd.read_{file_type}

  OTHER PROPS
    df.drop(['a','b',...]) - takes all other columns than the dropped ones
    df.drop("region", axis = 1, inplace = True)
      #inplace = True ensures that data frame operation is not performed and nothing is returned
      #{axis = 1} == {axis = 'columns'} & {axis = 0} == {axis = "rows"}
    df.rename(columns = {'a':'A',...}) - renames the columns
    df['A'] = df['A'].astype("int")

  DESCRIPTIVE
    df['Portability'].value_counts - unique value counts
    df['Portability'].value_counts.index.tolist() - unique value key names
    df['Portability'].unique() - gives all the unique values, same as above
    df['Portability'].nunique() - gives total no of unique values
    df['Portability'].isnull().sum() - gives total no of null cells in 'Portability' column
    df.dtypes - gives the type of data stored in each column
    df.shape - column * row
    df.shape[0] - size of rows
    df.shape[1] - size of columns
    df.columns - column names
    df.describe - describes data, like its mean, 75% values, etc.
    df.describe(include='all')
    df.info

  APPLY AND MAP
    df['quality'] = df['quality'].apply(lambda x:x*100)
    df['quality'] = df['quality'].map(lambda x:x*100)
    df.apply(lambda x:x*100)

  INDEXING SORTING SLICING {INDEX PROPS}
    import pandas as pd
    import numpy as np
    df = pd.DataFrame(np.random.rand(5,3), index=[5,3,2,4,1], columns = list('ABC'))

    # for a specific row
    print(df)
    print(df.loc[1]) #for a specific index calling wrt no
    print(df.iloc[1]) # for a specific index calling wrt location {location starts from 0}

    #Sorting
    print(df.sort_index())
    print(df.sort_index(ascending = False))




    #Slicing
    df = df.sort_index()
    print(df.head(3))
    print(df.tail(3))
    print(df[1:4])

  MISSING VALUES
    import pandas as pd
    import numpy as np
    df = pd.DataFrame([[10,15,12], [np.NaN, 13, 10], [14, np.NaN, 13], [np.NaN, np.NaN, 14], [13,12,11]], index = [1,2,3,4,5], columns = ['A', 'B', 'C'])
    print(df)



    df = df['col name']
    df4 = df.fillna(method = 'ffill')
    print(df4)
    df5 = df.fillna(method = 'bfill')
    print(df5)
    df3 = df.fillna(0)
    print(df3)
    df6 = df.fillna(df.mean()) #or df.median / df.mode() / df.max() / df.min()
    print(df6)
    df10 = df.replace(np.nan, df.mean())

    print(df.isnull().sum())
    #df7 = df.fillna(subset = ['B']) ???????????????????????????????????????
    #print(df7) ??

    df1 = df.dropna(subset = ['col name'], axis = 0 , inplace - True) # list wise deletion
    print(df1)
    df2 = df.dropna(subset = ['col name'], axis = 1 , inplace - True) # pair wise deletion
    print(df2)

    df = df['col name']
    df4 = df.fillna(method = 'ffill')
    print(df4)
    df5 = df.fillna(method = 'bfill')
    print(df5)
    df3 = df.fillna(0)
    print(df3)
    df6 = df.fillna(df.mean()) / df.median / df.mode() / df.max() / df.min()
    print(df6)
    df10 = df.replace(np.nan, df.mean())
    print(df10)
    df8 = df.fillna(df.mode().iloc[0])
    print(df8)

    print(df.isnull().sum())
    print(df.info())
    print(df.isna())
    df9 = df.dropna(subset = ['col name'], axis = 0/1)
    #df7 = df.fillna(subset = ['Col name'], df.mean()) ??
    #print(df7) ??

  GROUPING, FILTERING AND VALUE_COUNTS- {FOR COLUMN RELATION SHIPS}
    import pandas as pd
    import numpy as np
    df = pd.read_csv(r'C:\Users\DELL\Downloads\wine.csv')
    print(df.describe(include = 'all')) # include = 'all' implies all the columns must be considered for describing
    print(df.info())
    print(df[['pH', 'type']].groupby(['type'], as_index=False).mean())
    print(df[['pH', 'type']].groupby(['type'], as_index=True).mean())
    print(df[['type', 'quality', 'density']].groupby(['type', 'quality'], as_index = False).mean())
    print(df.groupby(['type'], as_index = False).mean())

    print(df[df['quality']>5][['pH', 'quality', 'density']].groupby(['quality'], as_index=False).mean())
    print(df[df['quality']>5][['pH', 'quality', 'density','type']].groupby(['quality', 'type'], as_index=False).mean())

    print(df[['density', 'pH', 'quality']].groupby(['quality'], as_index=True).agg([np.sum, np.mean, np.std]))

    print(df.groupby('quality').filter(lambda x: len(x)>=50)) # ??????????????????

  RELATION BETWEEN COLUMNS - USED FOR PLOTTING
    Refer to SEC - GROUPING + FILTERING TOO
    #df.corr() - gives us the correlation of each column with each other columns
    #plt.figure(figsize =(20,20))
     sns.heatmap(df.corr(), annot = True, cmap = 'coolwarm', linewidths = 2)
    # On basis on heatmap correlation b/w two columns we decide to draw a graph between them

  FOR ALPHABETICAL DATA
    FOR MAKING COLUMS FOR EACH DISTINCT ALPHABETICAL DATA = 4
      a = pd.get_dummies(df['a']) - #try and see
      df = pd.concat([df, a], axis = 1) - then df dataframe adds 'a' dataframe into it
      #pd.concat([df,a]) without axis parameter may concat in row
      # pd.append() works similar to pd.concat()
    FOR YES / NO = 2
      map1 = {'male':1, 'female': 0}
      df['gender'] = df['gender'].map(map1)
    LABEL ENCODER = MAKING ARBITARY NUMBERS FOR EACH COLUMN
      from sklearn.preprocessing import LabelEncoder
      outlook_at = LabelEncoder()
      df['Summary_a'] = outlook_at.fit_transform(a)
      df['D_Sum_b'] = outlook_at.fit_transform(b)
      df['Precip_c'] = outlook_at.fit_transform(c)

Numpy:
  to work with arrays.
  to operate on numerical python {sin, cos, pi}
  np.sin
  np.cos
  np.linspace(0,10,20) - 20 equally apced no's b/w 0 and 10
  np.radnom.randn(500).cumsum()
  Numpy_codes
      # array vs np.array
      import numpy as np
      l = range(1000)
      print(type(l))
      n = np.arange(1000)
      print(type(n))
      print('??????????????')
      S = np.random.rand(1000)
      L = [S]
      N = np.array(S)
      import sys
      print("{0} \n{1}".format(type(L), type(N)))
      print(sys.getsizeof(1)*len(L))
      print(N.size * N.itemsize)
      print('??????????????')

      # Storage:
        import sys
        l_storage = sys.getsizeof(1)*len(l)
        print('list: ',l_storage,  )
        n_storage = n.size * n.itemsize
        print('numpy: ',n_storage)

      # Time
        import time
        l1 = range(1000000)
        l2 = range(1000000)
        l3 = []
        start = time.time()
        for i in range(len(l1)):
            l3.append(l1[i] + l2[i])
        end = time.time()
        print("list: ", (end - start) * 1000)
        n1 = np.arange(1000000)
        n2 = np.arange(1000000)
        start2 = time.time()
        n3 = n1 + n2
        end2 = time.time()
        print('array: ', (end2 - start2) * 1000)

      # Creating specific lists {random}
        print(np.empty(5)) #it is used to fit elements in empty np array using range  # returns previously allocated elements in similar dimentional arrays
        print(np.empty((5,3)))

        print(np.ones(5))
        print(np.ones((5,3)))

        print(np.arange(1,10,2)) #(start, stop, step)  #similar to range func

        print(np.linspace(1,10,10))

        print(np.random,randn(500).cumsum())

        #using random {# Here the code is not in python format}
          # rand = random
          np.random.seed(10)
          random(B) = 1 set with B number of elements { only + }
            random((a,b,c,d,e))  = a sets are formed {only +}
                             each of a set with b sets
                             each of b set with c sets
                             each of c set with d sets
                             each of d set has e elements in it
          rand(B) = 1 set with B number of elements { only +}
            rand(a,b,c,d,e) = a sets are formed {only +} ----- ERROR
                             each of a set with b sets
                             each of b set with c sets
                             each of c set with d sets
                             each of d set has e elements in it
          randn(B) = 1 set with B number of elements { + and - }
            randn(a,b,c,d,e) = a sets are formed ----- ERROR
                             each of a set with b sets
                             each of b set with c sets
                             each of c set with d sets
                             each of d set has e elements in it
          randint(B) = 1 element in range(B)
            randint(a,b) = 1 element between a and b
            randint(a,b,c) = c elements between a and b
            randint(A,B,(a,b,c,d,e)) = numbers between A and B form
                             a sets are formed {only +}
                             each of a set with b sets
                             each of b set with c sets
                             each of c set with d sets
                             each of d set has e elements in it
          x = [1,2,3,4,5,6,7,8,9]

          print(np.random.choice(x))

          print('Permutation: ', np.random.permutation(5))

          print('Before shuffle',x)
          np.random.shuffle(x)
          print('After shuffle',x)

      # Manipulations {nd_to_1d + slicing + concat + split}
        # 1D to nD
          n1 = np.arange(1,13,2)
          n2 = n1.reshape(2,3)
          print(n2) # reshaped (2,3) i.e 2x3 = 6 must be the number of elements in the 1D (1,13,2) array
          # nD to 1D
          print(n2.ravel())
          print(n2.flatten())
          # columns to rows and rows to columns
          print(n2.transpose())

        #Array slicing
          n = np.array([[1,2,3],[4,5,6],[7,8,9]])
          print(n)
          # for rows:
          print(n[0])
          print(n[0:2]) # first two
          # for columns
          print(n[:,0])
          print(n[:,0:2])

        # concatinating
          n1 = np.array([[1,2,3],[4,5,6],[7,8,9]])
          n2 = np.array([[1,2,3],[4,5,6],[7,8,9]])
          n = np.concatenate((n1,n2))
          print(n)
          n_v = np.vstack((n1,n2))
          print(n_v)
          n_h = np.hstack((n1,n2))
          print(n_h)

        # Splitting
          v_n = np.split(n_v,2)
          print(v_n)
          V_N = np.split(n_v,3, axis = 1)
          print(V_N)
          h_n = np.split(n_h,3)
          print(h_n)
          H_N = np.split(n_h,3, axis = 1)
          print(H_N)

      # Props
        n = np.array(np.random.random(10))
        N = np.array(np.random.rand(3,5))

        print(n.ndim)
        print(N.ndim)

        print(n.shape)
        print(N.shape)

      # Operations
        n = np.array([[1,2],[3,4]])
        N = np.array([[1,2],[3,4]])

        # print(n  +-*/  N)
        print(np.add(n,N))
        print(np.subtract(n,N))
        print(n.dot(N))

        print(n)
        print(n.max())
        print(n.min())
        print(n.max(axis = 1))
        print(n.min(axis = 1))
        print(n.max(axis = 0))
        print(n.min(axis = 0))
        print(n.argmax())
        print(n.argmin())

        # Many more
        nN = np.array(np.random.rand(3,5,5))
        print("sum:{0}, mean:{1}, sqrt:{2}, log:{3}, exp:{4}, std: {5}, log10{6}".format(np.sum(nN), np.mean(nN), np.sqrt(nN), np.log(nN), np.exp(nN), np.std(n), np.log10(n)))
        np.sum(n, axis = 0/1)

      # String Manipulation
        a = 'Pilla'
        b = 'Bunny'
        print(np.char.add(a,b))
        print(np.char.equal(a,b))
        print(np.char.upper(a))
        print(np.char.lower(b))
        print(np.char.replace(a,'l','L'))
        print(np.char.center(a,12,fillchar="*"))
        print(np.char.join([':', "/"], [a,b]))
        print(np.char.count(a,'l'))
        print(np.char.split(a, 'l'))
        #split line from string
        str3 = "abc \n 123"
        print (np.char.splitlines(str3))

      # Trig
        import matplotlib.pyplot as plt
        x = np.arange(0,2*np.pi,0.1)
        plt.plot(x, np.sin(x))
        plt.plot(x, np.cos(x))
        #plt.plot(x, np.tan(x))
        plt.show()
        plt.plot(x, np.tan(x))
        plt.show()

Matplotlib:
  for data visualization
  similar to MATLAB

  X AND Y
    plt.figure(figsize=(10,10)) --- size
    fig = plt.figure()
      ax1 = fig.add_axes([0,0,1,1])           #[0-x(leftmost_co-ord), 0-y(bottom_co-ord), 1-x(rightmost_co-ord), 1-y(top_co-ord)]
      ax2 = fif.add_axes([0.5,0.5,0.4,0.4])   #graph_of_{0.5 to 0.5+0.4 on x and y} inside graph_of_{0 to 1 on x and y}
    plt.xlim([0,1]) / plt.ylim([0,1])
    plt.ylim()
    plt.title('')
    plt.xlabel('') / plt.ylable('')
    plt.legend(loc='upper right')
    plt.show()

  PLOTS
    Here : x = range(len(y))
    plt.plot(x,y, color='') ---line
    plt.scatter(x,y, color='') --- points
    plt.bar(x,y) ---bar
    plt.barh(x,y) --- horizontal bar
    plt.pie(x, labels = leabels) --- pie
                                    E.x. :
                                    plt.figure(figsize=(7,7))
                                    x10 = [35, 25, 20, 20]
                                    labels = ['Computer', 'Electronics', 'Mechanical', 'Chemical']
                                    plt.pie(x10, labels=labels);
                                    plt.show()
    plt.boxplot(x) --- boxplot:
                      used to get visualization on distribution of values in a field or to compare the value trends in two / more fields
                      Q1 = lower quartile represent 25% of data's value
                      Q2 = median represent 50% of data's value
                      Q3 = upper quartile represent 75% of data's value
                      Maximum represent the maximum value
                      Minimum represent the min value
                      outliers represent the values beyond minimum and maximum {far from graph}
                      whiskers represent the remaining values
    plt.bar(range(len(y)), y, 'r')
    plt.bar(range(len(z)), z, 'b', bottom = y )

  plt properties:

    marker='*'/ color='red' / emap='viridis' or 'binary' or 'plt.cm.binary' /

  3D:
    ax = plt.axes(projection='3d')
    ax.plot3D(X,Y,Z,emap='')
    Images:
    plt.imshow(images[i], cmap = plt.cm.binary) --- to show Images
    plt.grid(True) --- to show grids
    plt.subplot(5,5,i+1) # 5,5=size , i+1 = index_no --- subplots size and no
    plt.xticks([]) / plt.yticks([]) --- ticks representation

Seaborn:
  link: https://towardsdatascience.com/seaborn-python-8563c3d0ad41
  on top of matplotlib - advanced version of matplotlib
  supports high level abstractions for multi plot grids

  Codes:
    import seaborn as sns
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    loaded = pd.read_csv('https://raw.githubusercontent.com/btkhimsar/DataSets/master/tips.csv')
    print(loaded.nunique())

    # Scatter plot
    sns.relplot(x="total_bill", y="tip",color = 'b', data=loaded);
    plt.show()
    sns.relplot(x="total_bill", y="tip", palette='viridis', hue='sex', style='time', size='size', sizes=(10,200), data=loaded)
    plt.show()

    # Lineplot
    # using loaded data
    sns.relplot(x="size", y="total_bill", hue ='day', kind='line', data=loaded);
    plt.title("loaded data")
    plt.show()
    # using random.cumsum()
    # A
    np.random.seed(42)
    sns.relplot(x=np.arange(500), y=np.random.randn(500).cumsum(), color='r', kind='line')
    plt.title("random A - cumsum")
    plt.show()
    # B - y manipulated wrt x
    np.random.seed(0)
    a = np.random.random((5,2))
    print(a)
    data = pd.DataFrame(a.cumsum(axis=0), columns=['x', 'y'])
    print(data)
    sns.relplot(x='x', y='y', data=data, kind='line')
    plt.title("random B - cumsum \n y manipulated wrt x")
    plt.show()

    # using dict = y manipulated wrt x
    diction = dict(key = np.arange(500), value=np.random.randn(500).cumsum())
    data = pd.DataFrame(diction)
    print(data)
    sns.relplot(x='key', y='value', data=data, kind='line')
    plt.title("dict")
    plt.show()

    # Getting dependancy of columns
    plt.figure(figsize=([10,10]))
    sns.heatmap(loaded.corr(), annot = True, cmap = 'coolwarm', linewidths = 2)
    plt.title('Heat Plot')
    plt.show()
    # point distribution w.r.t columns
    sns.pairplot(loaded[['pH', 'sulphates', 'alcohol', 'quality']])
    plt.title('Pair Plot')
    plt.show()

Scipy:
    on top of numpy - advanced version of numpy
    scientific operations with more features, but slow in speed than numpy

Sklearn:
  link: https://scikit-learn.org/stable/
  on top of scipy, numpy, matplotlib

northeast...


Excel:
  import numpy as np
  import pandas as pd

  # Creating a DataFrame
  data = {
      'Name': ['Alice', 'In', 'Charlie'],
      'Age': [25, 30, 28],
      'City': ['New York', 'San Francisco', 'Los Angeles']
  }
  df = pd.DataFrame(data)
  excel_file_path = r'C:\Users\DELL\Desktop\B tech 1\Excel\from_python.xlsx'
  df.to_excel(excel_file_path, index=False, sheet_name='Sheet1')

  data = {
      'Name': ['John', 'Cena', 'WWW'],
      'Age': [25, 30, 28],
      'City': ['New York', 'San Francisco', 'Los Angeles']
  }
  excel_file_path = r'C:\Users\DELL\Desktop\B tech 1\Excel\from_python.xlsx'
  with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
      df.to_excel(writer, index=False, sheet_name='Sheet2')
      # You can add more sheets and customize the Excel file here

    """
    return a

