#!/bin/bash -x
# Author: Kun Huang <academicgareth@gmail.com>

echo "Hello, scalpels ci"
sca setup -d /opt/stack/data/scalpels/scripts

function debug_msg {
    sudo netstat -nltp
    sudo ps axf
    sudo env
    env
}

function basic_test {
    sca start -a rpc -a rabbit -a traffic

    source /opt/stack/new/devstack/openrc admin admin
    sca load --storm
    sleep 10
    sca stop

    echo waiting agent write data into db before report
    sleep 20

    sca report
    sca result --list
}

function report_html_test {
    sca start -a rpc
    sca load --storm
    sleep 120
    sca stop

    for i in `sca result --list --short | tail -n2`; do
        sca result $i --html > $BASE/logs/scalpels-result-$i.html
    done
    sca report --html > $BASE/logs/scalpels-report.html
}

function stap_test {
    scal_ci=$BASE/new/scalpels/tests/ci/
    sudo stap -vvv $scal_ci/pyfunc.stp -c "$DATA_DIR/cpython_build/bin/python $scal_ci/test-func.py"
}

debug_msg
basic_test
report_html_test
stap_test
