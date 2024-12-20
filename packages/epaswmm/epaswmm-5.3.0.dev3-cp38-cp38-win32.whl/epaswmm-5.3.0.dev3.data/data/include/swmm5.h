//-----------------------------------------------------------------------------
//   swmm5.h
//
//   Project: EPA SWMM5
//   Version: 5.2
//   Date:    11/01/21  (Build 5.2.0)
//   Author:  L. Rossman
//
//   Prototypes for SWMM5 API functions.
//   
//   Update History
//   ==============
//   Build 5.3.0:
//   - Added new functions to support saving hotstart files at specific times.
//   - Expansions to the SWMM API to include attributes of more objects and water quality.
//
//-----------------------------------------------------------------------------

#ifndef SWMM5_H
#define SWMM5_H

// --- define WINDOWS

#undef WINDOWS
#ifdef _WIN32
  #define WINDOWS
#endif
#ifdef __WIN32__
  #define WINDOWS
#endif

// --- define DLLEXPORT

#ifdef WINDOWS
    #define DLLEXPORT __declspec(dllexport) __stdcall
#else
    #define DLLEXPORT
#endif

// --- use "C" linkage for C++ programs

#ifdef __cplusplus
extern "C" { 
#endif

typedef enum {
    swmm_GAGE,
    swmm_SUBCATCH,
    swmm_NODE,
    swmm_LINK,
    swmm_POLLUTANT,
    swmm_LANDUSE,
    swmm_TIME_PATTERN,
    swmm_CURVE,
    swmm_TIMESERIES,
    swmm_CONTROL_RULE,
    swmm_TRANSECT,
    swmm_AQUIFER,
    swmm_UNIT_HYDROGRAPH,
    swmm_SNOWPACK,
    smmm_XSECTION_SHAPE,
    swmm_LID,
    swmm_STREET,
    swmm_INLET,
    swmm_SYSTEM   = 100
} swmm_Object;

typedef enum {
    swmm_JUNCTION = 0,
    swmm_OUTFALL  = 1,
    swmm_STORAGE  = 2,
    swmm_DIVIDER  = 3
} swmm_NodeType;

typedef enum {
    swmm_CONDUIT = 0,
    swmm_PUMP    = 1,
    swmm_ORIFICE = 2,
    swmm_WEIR    = 3,
    swmm_OUTLET  = 4
} swmm_LinkType;

typedef enum {
    swmm_GAGE_TOTAL_PRECIPITATION = 100,
    swmm_GAGE_RAINFALL = 101,
    swmm_GAGE_SNOWFALL = 102,
} swmm_GageProperty;

typedef enum {
    swmm_SUBCATCH_AREA      = 200,
    swmm_SUBCATCH_RAINGAGE  = 201,
    swmm_SUBCATCH_RAINFALL  = 202,
    swmm_SUBCATCH_EVAP      = 203,
    swmm_SUBCATCH_INFIL     = 204,
    swmm_SUBCATCH_RUNOFF    = 205,
    swmm_SUBCATCH_RPTFLAG   = 206,
    swmm_SUBCATCH_WIDTH     = 207,
    swmm_SUBCATCH_SLOPE     = 208,
    swmm_SUBCATCH_CURB_LENGTH = 209,
    swmm_SUBCATCH_API_RAINFALL = 210,
    swmm_SUBCATCH_API_SNOWFALL = 211,
    swmm_SUBCATCH_POLLUTANT_BUILDUP  = 212,
    swmm_SUBCATCH_EXTERNAL_POLLUTANT_BUILDUP = 213,
    swmm_SUBCATCH_POLLUTANT_RUNOFF_CONCENTRATION = 214,
    swmm_SUBCATCH_POLLUTANT_PONDED_CONCENTRATION = 215,
    swmm_SUBCATCH_POLLUTANT_TOTAL_LOAD = 216,
} swmm_SubcatchProperty;

typedef enum {
    swmm_NODE_TYPE     = 300,
    swmm_NODE_ELEV     = 301,
    swmm_NODE_MAXDEPTH = 302,
    swmm_NODE_DEPTH    = 303,
    swmm_NODE_HEAD     = 304,
    swmm_NODE_VOLUME   = 305,
    swmm_NODE_LATFLOW  = 306,
    swmm_NODE_INFLOW   = 307,
    swmm_NODE_OVERFLOW = 308,
    swmm_NODE_RPTFLAG  = 309,
    swmm_NODE_SURCHARGE_DEPTH = 310,
    swmm_NODE_PONDED_AREA = 311,
    swmm_NODE_INITIAL_DEPTH = 312,
    swmm_NODE_POLLUTANT_CONCENTRATION = 313,
    swmm_NODE_POLLUTANT_LATMASS_FLUX = 314,
} swmm_NodeProperty;

typedef enum {
    swmm_LINK_TYPE       = 400,
    swmm_LINK_NODE1      = 401,
    swmm_LINK_NODE2      = 402,
    swmm_LINK_LENGTH     = 403,
    swmm_LINK_SLOPE      = 404,
    swmm_LINK_FULLDEPTH  = 405,
    swmm_LINK_FULLFLOW   = 406,
    swmm_LINK_SETTING    = 407,
    swmm_LINK_TIMEOPEN   = 408,
    swmm_LINK_TIMECLOSED = 409,
    swmm_LINK_FLOW       = 410,
    swmm_LINK_DEPTH      = 411,
    swmm_LINK_VELOCITY   = 412,
    swmm_LINK_TOPWIDTH   = 413,
    swmm_LINK_RPTFLAG    = 414,
    swmm_LINK_OFFSET1    = 415,
    swmm_LINK_OFFSET2    = 416,
    swmm_LINK_INITIAL_FLOW = 417,
    swmm_LINK_FLOW_LIMIT = 418,
    swmm_LINK_INLET_LOSS = 419,
    swmm_LINK_OUTLET_LOSS = 420,
    swmm_LINK_AVERAGE_LOSS = 421,
    swmm_LINK_SEEPAGE_RATE = 422,
    swmm_LINK_HAS_FLAPGATE = 423,
    swmm_LINK_POLLUTANT_CONCENTRATION = 424,
    swmm_LINK_POLLUTANT_LOAD = 425,
    swmm_LINK_POLLUTANT_LATMASS_FLUX = 426,
} swmm_LinkProperty;

typedef enum {
    swmm_STARTDATE = 0,
    swmm_CURRENTDATE = 1,
    swmm_ELAPSEDTIME = 2,
    swmm_ROUTESTEP = 3,
    swmm_MAXROUTESTEP = 4,
    swmm_REPORTSTEP = 5,
    swmm_TOTALSTEPS = 6,
    swmm_NOREPORT = 7,
    swmm_FLOWUNITS = 8,
    swmm_ENDDATE = 9,
    swmm_REPORTSTART = 10,
    swmm_UNITSYSTEM = 11,
    swmm_SURCHARGEMETHOD = 12,
    swmm_ALLOWPONDING = 13,
    swmm_INERTIADAMPING = 14,
    swmm_NORMALFLOWLTD = 15,
    swmm_SKIPSTEADYSTATE = 16,
    swmm_IGNORERAINFALL = 17,
    swmm_IGNORERDII = 18,
    swmm_IGNORESNOWMELT = 19,
    swmm_IGNOREGROUNDWATER = 20,
    swmm_IGNOREROUTING = 21,
    swmm_IGNOREQUALITY = 22,
    swmm_ERROR_CODE = 23,
    swmm_RULESTEP= 24,
    swmm_SWEEPSTART = 25,
    swmm_SWEEPEND = 26,
    swmm_MAXTRIALS = 27,
    swmm_NUMTHREADS = 28,
    swmm_MINROUTESTEP = 29,
    swmm_LENGTHENINGSTEP = 30,
    swmm_STARTDRYDAYS = 31,
    swmm_COURANTFACTOR = 32,
    swmm_MINSURFAREA = 33,
    swmm_MINSLOPE = 34,
    swmm_RUNOFFERROR = 35,
    swmm_FLOWERROR = 36,
    swmm_QUALERROR = 37,
    swmm_HEADTOL = 38,
    swmm_SYSFLOWTOL = 39,
    swmm_LATFLOWTOL = 40,
} swmm_SystemProperty;



typedef enum {
    swmm_CFS = 0,  // cubic feet per second
    swmm_GPM = 1,  // gallons per minute
    swmm_MGD = 2,  // million gallons per day
    swmm_CMS = 3,  // cubic meters per second
    swmm_LPS = 4,  // liters per second
    swmm_MLD = 5   // million liters per day
} swmm_FlowUnitsProperty;


typedef enum {
    // ... API Errors
    ERR_API_NOT_OPEN = -999901,
    ERR_API_NOT_STARTED = -999902,
    ERR_API_NOT_ENDED = -999903,
    ERR_API_OBJECT_TYPE = -999904,
    ERR_API_OBJECT_INDEX = -999905,
    ERR_API_OBJECT_NAME = -999906,
    ERR_API_PROPERTY_TYPE = -999907,
    ERR_API_PROPERTY_VALUE = -999908,
    ERR_API_TIME_PERIOD = -999909,
    ERR_API_HOTSTART_FILE_OPEN = -999910,
    ERR_API_HOTSTART_FILE_FORMAT= -999911,
    ERR_API_IS_RUNNING = -999912,
} swmm_API_Errors;

typedef void (*progress_callback)(double progress);

int    DLLEXPORT swmm_run(const char *inputFile, const char *reportFile, const char *outputFile);
int    DLLEXPORT swmm_run_with_callback(const char *inputFile, const char *reportFile, const char *outputFile, progress_callback callback);
int    DLLEXPORT swmm_open(const char *inputFile, const char *reportFile, const char *outputFile);
int    DLLEXPORT swmm_start(int saveFlag);
int    DLLEXPORT swmm_step(double *elapsedTime);
int    DLLEXPORT swmm_stride(int strideStep, double *elapsedTime);
int    DLLEXPORT swmm_useHotStart(const char* hotStartFile);
int    DLLEXPORT swmm_saveHotStart(const char* hotStartFile);
int    DLLEXPORT swmm_end(void);
int    DLLEXPORT swmm_report(void);
int    DLLEXPORT swmm_close(void);

int    DLLEXPORT swmm_getMassBalErr(float *runoffErr, float *flowErr, float *qualErr);
int    DLLEXPORT swmm_getVersion(void);
int    DLLEXPORT swmm_getError(char *errMsg, int msgLen);
int    DLLEXPORT swmm_getErrorFromCode(int error_code, char *outErrMsg[1024]);
int    DLLEXPORT swmm_getWarnings(void);

int    DLLEXPORT swmm_getCount(int objType);
int    DLLEXPORT swmm_getName(int objType, int index, char *name, int size);
int    DLLEXPORT swmm_getIndex(int objType, const char *name);
double DLLEXPORT swmm_getValue(int property, int index);
double DLLEXPORT swmm_getValueExpanded(int objType, int property, int index, int subIndex);
int    DLLEXPORT swmm_setValue(int property, int index,  double value);
int    DLLEXPORT swmm_setValueExpanded(int objType, int property, int index, int subIndex, double value);
double DLLEXPORT swmm_getSavedValue(int property, int index, int period);
void   DLLEXPORT swmm_writeLine(const char *line);
void   DLLEXPORT swmm_decodeDate(double date, int *year, int *month, int *day,
                 int *hour, int *minute, int *second, int *dayOfWeek);
double DLLEXPORT swmm_encodeDate(int year, int month, int day,
                 int hour, int minute, int second);


#ifdef __cplusplus 
}   // matches the linkage specification from above */ 
#endif

#endif //SWMM5_H
