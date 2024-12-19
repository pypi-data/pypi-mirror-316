#ifndef CASM_clexmonte_events_event_data_json_io
#define CASM_clexmonte_events_event_data_json_io

#include "casm/configuration/occ_events/io/json/OccEvent_json_io.hh"

namespace CASM {
class jsonParser;
template <typename T>
class InputParser;

namespace clexmonte {
struct EventID;
struct EventState;
struct EventData;
struct PrimEventData;
struct EventFilterGroup;

// -- EventState --

jsonParser &to_json(EventState const &event_state, jsonParser &json);

jsonParser &to_json(EventState const &event_state, jsonParser &json,
                    PrimEventData const &prim_event_data);

jsonParser &to_json(EventState const &event_state, jsonParser &json,
                    EventData const &event_data,
                    PrimEventData const &prim_event_data);

// -- EventData --

jsonParser &to_json(EventData const &event_data, jsonParser &json);

jsonParser &to_json(EventData const &event_data, jsonParser &json,
                    PrimEventData const &prim_event_data);

// -- PrimEventData --

jsonParser &to_json(PrimEventData const &prim_event_data, jsonParser &json);

jsonParser &to_json(
    clexmonte::PrimEventData const &data, jsonParser &json,
    std::optional<std::reference_wrapper<occ_events::OccSystem const>>
        event_system,
    occ_events::OccEventOutputOptions const &options =
        occ_events::OccEventOutputOptions());

// -- EventID --

jsonParser &to_json(clexmonte::EventID const &event_id, jsonParser &json);

void parse(InputParser<clexmonte::EventID> &parser);

void from_json(clexmonte::EventID &event_id, jsonParser const &json);

// -- EventFilterGroup --

jsonParser &to_json(clexmonte::EventFilterGroup const &filter,
                    jsonParser &json);

void parse(InputParser<clexmonte::EventFilterGroup> &parser);

void from_json(clexmonte::EventFilterGroup &filter, jsonParser const &json);

}  // namespace clexmonte
}  // namespace CASM

#endif
