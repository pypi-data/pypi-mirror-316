from bqSQLrunner import bqSQLrunner


def initBqSQLrunner(sqldir=None, workdir=None, project=None, dataset=None, variables=None,
                    fromstep=None, tostep=None, jsonvars=None, dryrun=False, fromScratch=False,
                    service_account=None):
    BqSQLrunner = bqSQLrunner(sqldir=sqldir, workdir=workdir, project=project, dataset=dataset, variables=variables,
                                          fromstep=fromstep, tostep=tostep, jsonvars=jsonvars,dryrun=dryrun,fromScratch=fromScratch,
                                          service_account=service_account)
    return BqSQLrunner