# plugin.sh - DevStack plugin.sh dispatch script Scalpels

SCALPELS_DIR=$DEST/scalpels
SCALPELS_REPO=${SCALPELS_REPO:-${GIT_BASE}/openstack/scalpels.git}
SCALPELS_BRANCH=${SCALPELS_BRANCH:-master}
SCALPELS_DATA_DIR=$DATA_DIR/scalpels/scripts

function install_scalpels {
    git_clone $SCALPELS_REPO $SCALPELS_DIR $SCALPELS_BRANCH
    setup_develop $SCALPELS_DIR
}

function init_scalpels {
    echo "run sca setup later"
    install -d $SCALPELS_DATA_DIR
    install -t $SCALPELS_DATA_DIR $SCALPELS_DIR/scripts/*
}

function start_scalpels {
    sca-manage setup -d /opt/stack/data/scalpels/scripts
    run_process scalpels "sca-agent"
}

function stop_scalpels {
    stop_process scalpels
}

function configure_scalpels {
    echo "nothing need config now."
}

function install_systemtap {
    old_dir=`pwd`
    cd $DATA_DIR
    wget https://sourceware.org/systemtap/ftp/releases/systemtap-2.5.tar.gz
    tar zxf systemtap-2.5.tar.gz
    wget https://fedorahosted.org/releases/e/l/elfutils/0.158/elfutils-0.158.tar.bz2
    tar jxf elfutils-0.158.tar.bz2
    cd systemtap-2.5
    ./configure  "--with-elfutils=$DATA_DIR/elfutils-0.158" --prefix=/usr/
    make
    sudo make install
    sudo stap -e 'probe begin { printf("Hello, World!\n"); exit() }'
    cd $old_dir
}

function install_dtrace_python {
    old_dir=`pwd`
    cd $DATA_DIR

    wget https://github.com/python/cpython/archive/ad609d460a207bc12ca83b43ab764ea58bd013ab.zip -O cpython.zip
    wget https://raw.githubusercontent.com/pyKun/openstack-systemtap-toolkit/master/cpython-patch/python_dtrace-2_7_9-enhanced.patch -O python_dtrace-2_7_9-enhanced.patch
    unzip cpython.zip
    mv ./cpython-ad609d460a207bc12ca83b43ab764ea58bd013ab ./cpython
    cd cpython

    git init
    git apply ../python_dtrace-2_7_9-enhanced.patch

    #sudo rm -rf /usr/local/lib/python2.7
    autoconf
    ./configure "--prefix=$DATA_DIR/cpython_build/" '--with-dtrace' '--enable-ipv6' '--enable-unicode=ucs2' '--with-dbmliborder=bdb:gdbm' '--with-system-expat' '--with-system-ffi' '--with-fpectl'
    make -j && make install

    cd $DATA_DIR
    ./cpython_build/bin/python -c "import sys"
    sudo stap -l 'process("./cpython_build/bin/python").mark("*")'
    cd $old_dir
}

# check for service enabled
if is_service_enabled scalpels; then

    if [[ "$1" == "stack" && "$2" == "pre-install" ]]; then
        # Set up system services
        echo_summary "Configuring system services scalpels"
        if is_ubuntu; then
            install_package autoconf automake gcc m4
            install_systemtap
            install_dtrace_python
        fi

    elif [[ "$1" == "stack" && "$2" == "install" ]]; then
        # Perform installation of service source
        echo_summary "Installing scalpels"
        install_scalpels

    elif [[ "$1" == "stack" && "$2" == "post-config" ]]; then
        # Configure after the other layer 1 and 2 services have been configured
        echo_summary "Configuring scalpels"
        configure_scalpels

    elif [[ "$1" == "stack" && "$2" == "extra" ]]; then
        # Initialize and start the scalpels service
        echo_summary "Initializing scalpels"
        init_scalpels
        start_scalpels
    fi

    if [[ "$1" == "unstack" ]]; then
        # Shut down scalpels services
        # no-op
        stop_scalpels
    fi

    if [[ "$1" == "clean" ]]; then
        # Remove state and transient data
        # Remember clean.sh first calls unstack.sh
        # no-op
        :
    fi
fi
