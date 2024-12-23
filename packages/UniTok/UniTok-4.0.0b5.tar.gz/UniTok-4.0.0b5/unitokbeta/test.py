import pandas as pd

from custom_tokenizer.json_entity_tokenizer import JsonEntitiesTokenizer
from unitokbeta.tokenizer import BertTokenizer, TransformersTokenizer, EntityTokenizer
from unitokbeta.unitok import UniTok


def tokenize():

    df = pd.read_csv(
        filepath_or_buffer='../news-sample.tsv',
        sep='\t',
        names=['nid', 'category', 'subcategory', 'title', 'abstract', 'url', 'tit_ent', 'abs_ent'],
        usecols=['nid', 'category', 'subcategory', 'title', 'abstract'],
    )

    # if abstract is empty, set it to empty string
    df['abstract'] = df['abstract'].fillna('')

    with UniTok() as ut:  # type: UniTok
        # define vocabularies and tokenizers under the current unitok instance
        bert_tokenizer = BertTokenizer(vocab='bert')
        llama_tokenizer = TransformersTokenizer(vocab='llama', key='huggyllama/llama-7b')
        category_tokenizer = EntityTokenizer(vocab='category')
        subcategory_tokenizer = EntityTokenizer(vocab='subcategory')

        ut.add_job(tokenizer=bert_tokenizer, column='title', name='title@bert', truncate=20)
        ut.add_job(tokenizer=llama_tokenizer, column='title', name='title@llama', truncate=20)
        ut.add_job(tokenizer=bert_tokenizer, column='abstract', name='abstract@bert', truncate=50)
        ut.add_job(tokenizer=llama_tokenizer, column='abstract', name='abstract@llama', truncate=50)
        ut.add_job(tokenizer=category_tokenizer)
        ut.add_job(tokenizer=bert_tokenizer, column='category', name='category@bert')
        ut.add_job(tokenizer=llama_tokenizer, column='category', name='category@llama')
        ut.add_job(tokenizer=subcategory_tokenizer)
        ut.add_job(tokenizer=bert_tokenizer, column='subcategory', name='subcategory@bert')
        ut.add_job(tokenizer=llama_tokenizer, column='subcategory', name='subcategory@llama')
        ut.add_job(tokenizer=EntityTokenizer(vocab='nid'))
        ut.add_index_job(name='index')

    ut.tokenize(df).save('here')


def add_column():
    df = pd.read_csv(
        filepath_or_buffer='../news-sample.tsv',
        sep='\t',
        names=['nid', 'category', 'subcategory', 'title', 'abstract', 'url', 'tit_ent', 'abs_ent'],
        usecols=['tit_ent'],
    )

    with UniTok.load('here') as ut:
        ut.add_job(tokenizer=JsonEntitiesTokenizer(vocab='bert'), column='tit_ent', truncate=50)

    ut.tokenize(df).save('here')


def transform():
    df = pd.read_csv(
        filepath_or_buffer='../news-sample.tsv',
        sep='\t',
        names=['nid', 'category', 'subcategory', 'title', 'abstract', 'url', 'tit_ent', 'abs_ent'],
    )
    df.to_csv('../news-sample-format.csv', sep='\t')


# transform()
tokenize()
# add_column()

# with UniTok.load('here', tokenizer_lib='custom_tokenizer') as ut:
#     print(ut.meta.tokenizers)


"""
unitok ../news_sample.tsv --depot here --tokenizer.classname jsonentities --column abs_ent --truncate 50 --lib custom_tokenizer 
"""
