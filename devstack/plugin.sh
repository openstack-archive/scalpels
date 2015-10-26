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

function configure_scalpels {
    echo "nothing need config now."
}

# check for service enabled
if is_service_enabled scalpels; then

    if [[ "$1" == "stack" && "$2" == "pre-install" ]]; then
        # Set up system services
        echo_summary "Configuring system services scalpels"

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
    fi

    if [[ "$1" == "unstack" ]]; then
        # Shut down scalpels services
        # no-op
        :
    fi

    if [[ "$1" == "clean" ]]; then
        # Remove state and transient data
        # Remember clean.sh first calls unstack.sh
        # no-op
        :
    fi
fi
