/**
 * Created by dfarrell on 7/24/16.
 */

(function($) {
    "use strict";

    var model,
        view,
        controller;

    // create the model
    model = (function() {
        var $event_pump = $("body");

        // return the public API
        return {
            get_names: function(lname) {
                var options = {
                    method: "GET",
                    url: "api/names" + (lname ? "/" + lname : ""),
                    dataType: "json",
                    contentType: "application/json"
                };
                $.ajax(options)
                    .done(function(data) {
                        $event_pump.trigger("get_names", {
                            names_list: data
                        });
                    })
                    .fail(function(jqXHR, textStatus, errorThrown) {
                        alert("failed to get names: " + textStatus);
                    });
            },
            update_name: function(data) {
                var options = {
                    method: "PUT",
                    url: "api/names" + (data.lname ? "/" + data.lname : ""),
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify(data)
                };
                $.ajax(options)
                    .done(function(data) {
                        $event_pump.trigger("update_name", {
                            names_list: data
                        });
                    })
                    .fail(function(jqXHR, textStatus, errorThrown) {
                        alert("failed to get names: " + textStatus);
                    });
            },
            create_name: function(data) {
                var options = {
                    method: "POST",
                    url: "api/names",
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify(data)
                };
                $.ajax(options)
                    .done(function(data) {
                        $event_pump.trigger("create_name", {
                            names_list: data
                        });
                    })
                    .fail(function(jqXHR, textStatus, errorThrown) {
                        alert("failed to get names: " + textStatus);
                    });
            },
            delete_name: function(lname) {
                var options = {
                    method: "DELETE",
                    url: "api/names" + (lname ? "/" + lname : ""),
                    dataType: "json",
                    contentType: "application/json"
                };
                $.ajax(options)
                    .done(function(data) {
                        $event_pump.trigger("delete_name", {
                            names_list: data
                        });
                    })
                    .fail(function(jqXHR, textStatus, errorThrown) {
                        alert("failed to get names: " + textStatus);
                    });
            }
        };
    }());

    // create the view
    view = (function() {
        var $names_list = $("#names_list"),
            $fname = $("#fname"),
            $lname = $("#lname");

        // return the public API
        return {
            reset: function() {
                $lname.val("").blur();
                $fname.val("").blur()
                setTimeout(function() {
                    focus();
                }, 50);
            },
            update_names_list: function(names_list) {
                var source = $("#update_names_template").html(),
                    template = Handlebars.compile(source),
                    html = template(names_list);

                $names_list
                    .find("tbody")
                    .empty()
                    .append(html);
            },
            update_editor: function(fname, lname) {
                $fname.focus().val(fname);
                $lname.focus().val(lname);
            }
        };
    }());

    // create the controller
    controller = (function(m, v) {
        var $event_pump = $("body"),
            model = m,
            view = v,
            $fname = $("#fname"),
            $lname = $("#lname");

        // get the initial names list
        model.get_names();

        // initialize the view
        view.reset();

        // handle the user events
        $("#reset").on("click", function() {
            view.reset();
        });

        $("#update").on("click", function() {
            var data = {
                fname: $.trim($fname.val()),
                lname: $.trim($lname.val())
            }
            if (data.lname !== "") {
                model.update_name(data);
            } else {
                Materialize.toast("Last name not valid", 4000, "rounded");
            }
        })

        $("#create").on("click", function() {
            var data = {
                fname: $.trim($fname.val()),
                lname: $.trim($lname.val())
            };
            if (data.lname !== "" && data.fname !== "") {
                model.create_name(data);
            } else {
                Materialize.toast("Data incomplete", 4000, "rounded");
            }
        })

        $("#delete").on("click", function(e) {
            var $this = $(e.target),
                lname;

            lname = $.trim($("#lname").val());

            if (lname !== "") {
                model.delete_name(lname);
            } else {
                Materialize.toast("Last name not selected", 4000, "rounded");
            }
        });

        $("#names_list table").on("dblclick", "tr", function(e) {
            var $this = $(e.target),
                fname = "",
                lname = "";

            fname = $this.parent().find(".fname").text();
            lname = $this.parent().find(".lname").text();

            view.update_editor(fname, lname);
        });

        // handle the model events
        $event_pump.on("get_names", function(e, data) {
            // update the view with the names list data
            view.update_names_list(data);
        });

        $event_pump.on("update_name", function(e, data) {
            // refresh the list of data
            model.get_names();
            view.reset();
            Materialize.toast("Name updated successfully", 4000, "rounded");
        });

        $event_pump.on("create_name", function(e, data) {
            // refresh the list of names
            model.get_names();
            view.reset();
            Materialize.toast("Name created successfully", 4000, "rounded");
        })

        $event_pump.on("delete_name", function(e, data) {
            // refresh the list of names
            e.preventDefault();
            model.get_names();
            view.reset();
            Materialize.toast("Name deleted successfully", 4000, "rounded");
        })
    }(model, view));

}(jQuery));