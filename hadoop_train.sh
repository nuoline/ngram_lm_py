#!/bin/bash

python_path="/share/python26.tar.gz"
nwordseg="/zhaizhouwei/lib/nwordseg.tar.gz"

input_path="${your_home}/your_input"
lm_ngram_path="${your_home}/lm_ngram"

$HADOOP_HOME/bin/hadoop fs -test -e $lm_ngram_path
if [ $? -eq 0 ];then
    $HADOOP_HOME/bin/hadoop fs -rmr $lm_ngram_path
fi
#-D mapred.min.split.size=268435456 \
#-D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
#-D stream.num.map.output.key.fields=2 \
#-D mapred.text.key.partitioner.options=-k1,1 \
#-D mapred.text.key.comparator.options="-k1,1 -k2,2nr" \
# -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \

$HADOOP_HOME/bin/hadoop streaming \
    -D mapred.job.reduce.capacity=400 \
    -D mapred.job.map.capacity=400 \
    -D mapred.job.priority=NORMAL \
    -D mapred.reduce.tasks=1000 \
    -D stream.memory.limit=1500 \
    -D mapred.job.name="ngram_lm_task" \
    -input $input_path \
    -output $lm_ngram_path \
    -mapper "python26/bin/python26.sh lm_mapper.py" \
    -reducer "python26/bin/python26.sh lm_reducer.py" \
    -cacheArchive "${python_path}#python26" \
    -cacheArchive "${nwordseg}#nwordseg" \
    -file ./lm_mapper.py \
    -file ./lm_reducer.py
if [ $? -ne 0 ]; then
    exit 1
fi
