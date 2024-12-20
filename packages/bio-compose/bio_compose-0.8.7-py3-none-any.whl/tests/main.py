import os

from bio_compose import get_compatible_verification_simulators
from bio_compose.api import get_biomodel_file, get_biomodel_archive
from bio_compose.verifier import Verifier
from bio_compose.runner import SimulationRunner
from bio_compose.composer import Composer


TEST_DEST = './tests/outputs'
DEFAULT_START = 0
DEFAULT_DURATION = 10
DEFAULT_NSTEPS = 100
DEFAULT_SBML_SIMULATORS = ['amici', 'copasi', 'tellurium']
DEFAULT_SBML_TEST_FILE = './fixtures/sbml-core/BIOMD0000000001_url.xml'
DEFAULT_OMEX_TEST_FILE = './fixtures/sbml-core/BIOMD0000000001.omex'

BIOMODELS_TO_TEST = [
    'BIOMD0000000013',
    'BIOMD0000000019'
]

test_runner = SimulationRunner()
test_verifier = Verifier()
test_composer = Composer()


def test_get_compatible():
    # comp = get_compatible_verification_simulators(DEFAULT_OMEX_TEST_FILE)
    # assert len(comp)
    pass


def test_run_smoldyn():
    pass


def test_run_utc():
    pass 


def test_verify_sbml():
    # model_fp = "/Users/alexanderpatrie/Downloads/BIOMD0000000001_url.xml"
    # submission = test_verifier.verify_sbml(entrypoint=model_fp, start=DEFAULT_START, end=DEFAULT_DURATION, steps=DEFAULT_NSTEPS, simulators=DEFAULT_SBML_SIMULATORS)
    # print(submission)
    # return submission
    pass


def test_get_verify_output(id=None):
    job_id = id or 'verification-bio_check-request-5dc81721-9c0e-481e-aa71-14c4e58a37f4-9e1cd4ab-9079-4b8e-960b-c61faa264c1c'
    output = test_verifier.get_output(job_id=job_id)
    print(output)


def test_verify_omex():
    pass


def test_run_composition():
    pass


def test_get_biomodel_file(multiple: bool = False):
    model_query = 'BIOMD0000000044' if not multiple else BIOMODELS_TO_TEST
    fp = get_biomodel_file(model_query, TEST_DEST)
    print(fp)


def test_get_biomodel_archives():
    for model in BIOMODELS_TO_TEST:
        fp = get_biomodel_archive(model, TEST_DEST)
        print(f'For {model}: {fp}')





