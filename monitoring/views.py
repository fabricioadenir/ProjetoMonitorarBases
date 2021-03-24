from django.shortcuts import render, redirect
import json
from monitoring.general_statistics.monitoring_statistic import MonitoringStatistic
from monitoring.general_statistics.query_result_statistic import QueryResultsStatistic
from monitoring.general_statistics.code_coverage_statistic import CodeCoverageStatistic
from monitoring.general_statistics.routines_statistic import RoutineStatistic
import logging
# Create your views here.
from .models import Profile


logger = logging.getLogger(__name__)


def dashboard(request):
    logger.info("Carregando Pagina Dashboard...")
    monitoring = MonitoringStatistic()
    query_result = QueryResultsStatistic()
    code_coverage = CodeCoverageStatistic()
    routine = RoutineStatistic()

    context = {
        "registered_monitoring_count": monitoring.get_quantity_of_registered_monitoring(),
        "monitoring_count_running": routine.get_monitoring_count_running(),
        "count_sucess": query_result.get_quantity_of_results_with_success(),
        "count_error": query_result.get_quantity_of_results_with_errors(),
        "count_ag_ativation": monitoring.get_quantity_of_monitoring_waiting_for_activation(),
        "graphic_error": json.dumps(query_result.get_results()),
        "graphic_top_error": json.dumps(query_result.get_the_top_3_with_errors()),
        "graphic_coverage_level": json.dumps(code_coverage.exemplo())
    }

    return render(request, 'monitoring/index.html', context)


def login(request):
    return render(request, 'monitoring/login.html')


def user(request):
    try:
        logger.info("Buscando informações do usuário")
        profile = Profile.objects.get(username="usuario_exemplo")
    except Exception as e:
        logger.error(f"Erro ao buscar info do usuário. Detalhes: {e}")
        return redirect(dashboard)
    context = {
        "full_name": f"{profile.first_name} {profile.last_name}",
        "username": profile.username,
        "email": profile.email,
        "team": profile.team,
        "positon": profile.positon,
        "detail": profile.detail,
        "photo": profile.photo
    }
    return render(request, 'monitoring/user.html', context)
