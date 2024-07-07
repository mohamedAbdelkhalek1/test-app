# -*- coding: utf-8 -*-
from urllib.parse import parse_qs

from odoo import http
import json


def valid_response(data, status):
    response_body = {
        'message': 'Successful',
        'data': data
    }
    return http.request.make_json_response(response_body, status=status)


def invalid_response(error, status):
    response_body = {
        'error': error
    }
    return http.request.make_json_response(response_body, status=status)


class CourseAPI(http.Controller):

    @http.route('/v1/course', methods=["POST"], type="http", auth="none", csrf=False)
    def api_create_course(self):
        args = http.request.httprequest.data.decode()
        vals = json.loads(args)
        try:
            rec = http.request.env['test_app.course'].sudo().create(vals)
            if rec:
                return valid_response({'id': rec.id}, status=201)
        except Exception as error:
            return invalid_response(error, status=400)

    # @http.route('/v1/course/create/json', methods=["POST"], type="json", auth="none", csrf=False)
    # def api_create_course(self):
    #     args = http.request.httprequest.data.decode()
    #     vals = json.loads(args)
    #     rec = http.request.env['test_app.course'].sudo().create(vals)
    #     if rec:
    #         return {
    #             'message': 'The new course is created successfully'
    #         }

    @http.route('/v1/course/<int:course_id>', methods=["PUT"], type="http", auth="none", csrf=False)
    def api_update_course(self, course_id):
        try:
            course_id = http.request.env['test_app.course'].sudo().search([('id', '=', course_id)])
            if not course_id:
                return invalid_response('Invalid ID', status=400)
            args = http.request.httprequest.data.decode()
            vals = json.loads(args)
            course_id.write(vals)
            return valid_response({
                'id': course_id.id,
                'name': course_id.name
            }, status=200)
        except Exception as error:
            return invalid_response(error, status=400)

    # @http.route('/v1/course/<int:course_id>', methods=["PUT"], type="json", auth="none", csrf=False)
    # def api_update_course(self, course_id):
    #     try:
    #         course_id = http.request.env['test_app.course'].sudo().search([('id', '=', course_id)])
    #         if not course_id:
    #             return {
    #                 'error': 'Invalid ID'
    #             }
    #         args = http.request.httprequest.data.decode()
    #         vals = json.loads(args)
    #         course_id.write(vals)
    #         return {
    #             'message': 'The course is updated successfully'
    #             # 'id': course_id.id,
    #             # 'name': course_id.name
    #         }
    #     except Exception as error:
    #         return {
    #             'Error': error
    #         }

    @http.route('/v1/course/<int:course_id>', methods=["GET"], type="http", auth="none", csrf=False)
    def api_get_course(self, course_id):
        try:
            course_id = http.request.env['test_app.course'].sudo().search([('id', '=', course_id)])
            if not course_id:
                return invalid_response('Invalid ID', status=404)
            return valid_response({
                'id': course_id.id,
                'name': course_id.name,
                'description': course_id.description
            }, status=200)
        except Exception as error:
            return invalid_response(error, status=400)

    # @http.route('/v1/course/json/<int:course_id>', methods=["GET"], type="json", auth="none", csrf=False)
    # def api_get_course_json(self, course_id):
    #     try:
    #         course_id = http.request.env['test_app.course'].sudo().search([('id', '=', course_id)])
    #         if not course_id:
    #             return {
    #                 'error': 'Invalid ID',
    #             }
    #         return {
    #             'id': course_id.id,
    #             'name': course_id.name,
    #             'description': course_id.description
    #         }
    #     except Exception as error:
    #         return {
    #             'Error': error,
    #         }

    @http.route('/v1/course/<int:course_id>', methods=["DELETE"], type="http", auth="none", csrf=False)
    def api_delete_course(self, course_id):
        try:
            course_id = http.request.env['test_app.course'].sudo().search([('id', '=', course_id)])
            if not course_id:
                return invalid_response('Invalid ID', status=404)
            course_id.unlink()
            return valid_response('The course is deleted successfully', status=200)
        except Exception as error:
            return invalid_response(error, status=400)

    @http.route('/v1/course', methods=["GET"], type="http", auth="none", csrf=False)
    def api_get_courses(self):
        try:
            params = http.request.httprequest.query_string.decode('utf-8')
            # params_qs = parse_qs(params) # domain in form ('key': ['value'])
            domain_list = params.split('&')
            print(domain_list)
            for index in range(len(domain_list)):
                domain_list[index] = domain_list[index].partition('=')
            print(domain_list)
            # domain = []
            # if params.get('state'):
            #     domain += [('state', '=', params.get('state')[0])]
            course_ids = http.request.env['test_app.course'].sudo().search(domain_list)
            if not course_ids:
                return invalid_response('No Existing records', status=404)
            return valid_response([{
                'id': course_id.id,
                'name': course_id.name,
                'description': course_id.description,
                'state': course_id.state
            } for course_id in course_ids], status=200)
        except Exception as error:
            return invalid_response(error, status=400)
