import ligo.followup_advocate
from ligo.followup_advocate.test.test_tool import MockGraceDb


mockgracedb = MockGraceDb('https://gracedb.invalid/api/')
path = "ligo/followup_advocate/test/templates/"


def test_cbc_compose():
    text = ligo.followup_advocate.compose(
               'S1234', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'cbc_compose.txt', 'r') as file:
        assert text == file.read()


def test_burst_compose():
    text = ligo.followup_advocate.compose(
               'S2468', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'burst_compose.txt', 'r') as file:
        assert text == file.read()


def test_cwb_burst_compose():
    text = ligo.followup_advocate.compose(
               'S2469', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'cwb_burst_compose.txt', 'r') as file:
        assert text == file.read()


def test_skymap_update():
    text = ligo.followup_advocate.compose_update(
               'S5678', client=mockgracedb, remove_text_wrap=False,
               update_types=['sky_localization'])
    with open(path + 'skymap_update.txt', 'r') as file:
        assert text == file.read()


def test_raven_update():
    text = ligo.followup_advocate.compose_update(
               'S5678', client=mockgracedb, remove_text_wrap=False,
               update_types=['raven'])
    with open(path + 'raven_update.txt', 'r') as file:
        assert text == file.read()


def test_general_update():
    text = ligo.followup_advocate.compose_update(
               'S5678', client=mockgracedb, remove_text_wrap=False,
               update_types=['sky_localization', 'p_astro',
                             'em_bright', 'raven'])
    with open(path + 'general_update.txt', 'r') as file:
        assert text == file.read()


def test_classification_update():
    text = ligo.followup_advocate.compose_update(
               'S5678', client=mockgracedb, remove_text_wrap=False,
               update_types=['p_astro', 'em_bright'])
    with open(path + 'classification_update.txt', 'r') as file:
        assert text == file.read()


def test_ssm_compose():
    text = ligo.followup_advocate.compose(
               'S6789', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'ssm_compose.txt', 'r') as file:
        assert text == file.read()


def test_raven_with_initial_circular():
    text = ligo.followup_advocate.compose_raven(
               'S1234', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'raven_with_initial_circular.txt', 'r') as file:
        assert text == file.read()


def test_raven_with_snews():
    text = ligo.followup_advocate.compose_raven(
               'S2468', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'raven_with_snews.txt', 'r') as file:
        assert text == file.read()


def test_raven_without_initial_circular():
    text = ligo.followup_advocate.compose_raven(
               'S3456', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'raven_without_initial_circular.txt', 'r') as file:
        assert text == file.read()


def test_medium_latency_cbc_only_detection():
    text = ligo.followup_advocate.compose_grb_medium_latency(
               'E1235', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'medium_latency_cbc_only_detection.txt', 'r') as file:
        assert text == file.read()


def test_medium_latency_cbc_detection():
    text = ligo.followup_advocate.compose_grb_medium_latency(
               'E1234', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'medium_latency_cbc_detection.txt', 'r') as file:
        assert text == file.read()


def test_medium_latency_cbc_burst_detection():
    text = ligo.followup_advocate.compose_grb_medium_latency(
               'E1122', client=mockgracedb, remove_text_wrap=False,
               use_detection_template=True)
    with open(path + 'medium_latency_cbc_burst_detection.txt', 'r') as file:
        assert text == file.read()


def test_medium_latency_cbc_exclusion():
    text = ligo.followup_advocate.compose_grb_medium_latency(
               'E1134', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'medium_latency_cbc_exclusion.txt', 'r') as file:
        assert text == file.read()


def test_medium_latency_cbc_burst_exclusion():
    text = ligo.followup_advocate.compose_grb_medium_latency(
               'E2244', client=mockgracedb, remove_text_wrap=False,
               use_detection_template=True)
    with open(path + 'medium_latency_cbc_burst_exclusion.txt', 'r') as file:
        assert text == file.read()


def test_llama_neutrino_track():
    text = ligo.followup_advocate.compose_llama(
               'S2468', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'llama_neutrino_track.txt', 'r') as file:
        assert text == file.read()


def test_llama_icecube_alert():
    text = ligo.followup_advocate.compose_llama(
               'S2468', client=mockgracedb, remove_text_wrap=False,
               icecube_alert='IceCubeCascade-230430a')
    with open(path + 'llama_icecube_alert.txt', 'r') as file:
        assert text == file.read()


def test_retraction():
    text = ligo.followup_advocate.compose_retraction(
               'S1234', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'retraction.txt', 'r') as file:
        assert text == file.read()


def test_retraction_early_warning():
    text = ligo.followup_advocate.compose_retraction(
               'S5678', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'retraction_early_warning.txt', 'r') as file:
        assert text == file.read()
