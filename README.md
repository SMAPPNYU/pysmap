```
 ___ _ __ ___   __ _ _ __  _ __  _   _ 
/ __| '_ ` _ \ / _` | '_ \| '_ \| | | |
\__ \ | | | | | (_| | |_) | |_) | |_| |
|___/_| |_| |_|\__,_| .__/| .__/ \__, |
                    |_|   |_|    |___/ 
```
:snake: smappy is a high level toolkit for dealing with twitter data it also has a higher level interface for [smappdragon](https://github.com/SMAPPNYU/smappdragon). it aggregates functionality from the ld toolkit and functionality from our old util library smappPy.

you might ask the difference between, smappy and smappdragon. smappy is easier to use but less flexible/more rigid in its implementation. smappdragon is a flexible tool fro programmers to use, you can build arbitray filters for data, smappy is just a set of filters.

methods on smappdragon are lower level and more general. whereas methods on smappy would be specific and rigid. so for example on smappdragon, you could [get all the entities](https://github.com/SMAPPNYU/smappdragon#top_entities), on smappy you would have to ask for hashtags, mentions, etc. (which are all entities).

another example, something like [apply_labels](https://github.com/SMAPPNYU/smapp-toolkit#apply_labels) would go on smappdragon, not smappy.

#author

[yvan](https://github.com/yvan)