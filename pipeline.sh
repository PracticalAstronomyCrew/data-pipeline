# 1. Check if new observation has been made. Based on date (previous)
#    --> does folder exist ()
#    --> Use controller script return status: 0 means success, 42 means no observation made

# TODO: use full options
# TODO: make sure controller is visible in path
# TODO: figure out the logging interface
# old cron location /etc/cron.daily/dataserver3-sync
BASE_PATH=/net/dataserver3/data/users/sterrenwacht/obslog
LOG_DIR=$BASE_PATH/logs
mkdir -p $BASE_PATH  # ensure this directory exists
mkdir -p $LOG_DIR  # ensure this directory exists

# TODO: add actual path to the controller
CONTROLLER=./path/to/controller.py
python3 ${CONTROLLER} -u -b -s -r -a > $LOG_DIR/somelogfile.log

# 2. Add stuff to headers
# Potentially add to controller
#   - Observation Type --> /i/: static image, /g/: tracked image, ST-7 / STL... figure out types
#   - Weather Conditions ? --> are these added already?
#   - Airmass --> create from OBJECTRA & OBJECTDEC

# 3. Run astrometry on the reduced files --> if successful also add information to raw file
#                                        --> if it fails run it on the original data & mark / save for another run ????
# 4. If astrometry successful add:
#   - Airmass     --> update / create
#   - Target Name --> use astrometry tags & name resolve using simbad to get coordinates and therefore position in the image
#   - Object Type  (see target)
# 5. Pack all the updated/new headers as a list of dicts & send these to the VO server
