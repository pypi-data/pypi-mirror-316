# py_iec61850_cdc Task Tracker

See below for planned tasks and completed tasks tracking.

## ToDo

- Add extension functions
  - update() function to all types.
    - Updates mag based on instmag
    - Updates quality.validity_t and quality.detailqual based on rangec
- Tests
  - Build constructor tests for each type
  - Add RootModel iterator tests
- Add IEC 61850-7-3 specified functionality (possibly as py_iec61850_cdc.util functions).
    - Address methods for substitution values (e.g. SubstitutionCDC) to be triggered to non-process.
    - BCR-specific
        - Add a freezing method to BCR.
        - Add pulsQty to value calculations (see pulsQty description).
    - Figure out how Originator works and make sure we can set it properly.

## Stretch Targets
- Review pydnp3 timestamp type, and add to/from functions to IEC
- Add curve setting / evaluating functions (e.g. ANSI / IEC or polynomial).
- Finish field_validator / model_validator implementation of constraints for logical nodes

## Done

2024-12-22
- Created prescond.py to standardize constraint algorithms
- Optional / constraints complete / visually inspected
  - abstract.py
  - status.py
  - attributes/
  - measurand.py
  - controls.py
  - settings.py
  - description.py
  - service.py
  - logical_nodes.py 
- RootModels for list items (e.g. HMV), incl. export alias

2024-12-21
- Created general constructor from JSON
- Added factory_local and datetime functions to timestamp
- Updated namespaces
- Created Vector.x() and Vector.y() functions for transforms, and Vector.factory_from_xy()
- Add CalendarTime functions around Python datetime
- Added IEC 61850-7-2 Objects:
  - ReasonForInclusionInReport
  - ReasonForInclusionInLog
  - LCBLogEntryOptions
  - ACSIClassKind
- Added IEC 61850-7-4 Logical Nodes necessary to implement GGIO.
