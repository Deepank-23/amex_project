from src.preprocessing import preprocess
from src.economics import create_economics
from src.ltv import create_ltv
from src.evidence import create_evidence
from src.baseline087 import create_best087_score
from sextra.ranking import create_rank
from src.submission import create_submission
from src.debug import compare_scores
from src.baseline087 import create_best087

def run_pipeline(df):

    df = preprocess(df)

    df = create_economics(df)

    df = create_ltv(df)

    df = create_evidence(df)

    df = create_best087(df)

    return df